# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 22:19:11 2022

@author: lider
"""

import pandas as pd
import time
import zipfile
import os
import patoolib as pat

from selenium import webdriver
from selenium.webdriver.common.by import By

user = os.getlogin()
home = r'C:\Users\{}'.format(user)

#%% Scrapping -- Raspa os dados com o Selenium
 
def Scraper():
    
    '''Realizar uma raspagem bem simples dos dados do COVID-19'''
    
    driver = webdriver.Edge(r"C:\Users\lider\msedgedriver.exe")
    driver.get('https://covid.saude.gov.br')

    l = driver.find_element(By.XPATH,'/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/div[1]/div[2]/ion-button')

    l.click()

    time.sleep(20)

#%% Loader --> Carrega os dados

def loader():
    
    ''' Checa pelos dados de covid no diretório de download
    do usuário e extrai eles ao cwd. Teoricamente é possíve eliminar o segundo
    laço for se você trabalhar extraindo os dados do diretório de downloads 
    direto sem os extrair ao cwd.'''
    
    
    os.chdir(r'C:\Users\{}\Downloads'.format(user))
    aux = os.listdir()
    
    for i in aux:
     
        if i.lower().endswith('.zip') and 'HIST_PAINEL_COVID' in i:
         
            with zipfile.ZipFile(i,'r') as zf:
             
                os.chdir(home)
                zf.extractall()   
        
        elif i.lower().endswith('.rar') and 'HIST_PAINEL_COVID' in i:
            
            pat.extract_archive(i, outdir = home)
            

    csvs = []
    
    os.chdir(home)
    aux2 = os.listdir()
    
    for i in aux2:
    
        if 'HIST_PAINEL_COVIDBR' in i:
        
            csvs.append(i)
                        
    df20201 = pd.read_csv(csvs[0], sep = ';')
    df20202 = pd.read_csv(csvs[1], sep = ';')
    df20211 = pd.read_csv(csvs[2], sep = ';')
    df20212 = pd.read_csv(csvs[3], sep = ';')
    df20221 = pd.read_csv(csvs[4], sep = ';')
    df20222 = pd.read_csv(csvs[5], sep = ';')        

    dfs = list([df20201,df20202,df20211,df20212,df20221,df20222])
    
    return dfs

#%% Cleaner --> limpa os dados

def cleaner(df):
    
 '''Toma como input o df a ser limpado, como estamos limpando o mesmo df
    para datas diferentes o método é o mesmo. No processo de limpeza mantemos
    apenas os dados agregados ao Brasil e não regionais '''

 df = df[df.regiao == 'Brasil'].drop(columns = df.iloc[:, [0,1,2,3,4,5,6,-1]])
 df.set_index(pd.to_datetime(df.data), inplace = True)
 df.index.name = 'Date'
 df = df.drop(columns = 'data')
 
 return df

#%% Deleter --> deleta os csvs

def Deleter():
    
    ''' Deleta os arquivos na pasta de downloads e na pasta do
    cwd'''

    downdir = os.chdir(r'C:\Users\{}\Downloads'.format(user))
    downloads = os.listdir()

    for i in downloads:
    
        if 'HIST_PAINEL_COVIDBR' in i:
            
            os.remove(i)
           
           
    maindir = os.chdir(home)   
    lider = os.listdir()        

    for j in lider:
        
        if 'HIST_PAINEL_COVIDBR' in j:
           
          
            os.remove(j)       
            
#%% Run

Deleter()

Scraper()

dfs = loader()

Deleter()

#%% Análise

dfsclean = [cleaner(i) for i in dfs]

covid = pd.concat(dfsclean).fillna(0)
     
analise = covid[['casosNovos','obitosNovos']].rolling(7).mean().dropna()

    