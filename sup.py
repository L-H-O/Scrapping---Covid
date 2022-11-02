# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 20:52:32 2022

@author: lider
"""

import requests as req
import pandas as pd
import os
import zipfile

from io import BytesIO
 
user = os.getlogin()

home = r'C:\Users\{}'.format(os.getlogin())   

#%% Extrai a distribuição acumulada das doses das vacinas contra o Covid por pop em função do tempo

def CovidVac():

    # Organiza as pastas do csvs, devem ser baixados manualmente primeiro

    def Scraper():
 
        r = req.get('https://github.com/wcota/covid19br-vac/archive/refs/heads/main.zip', verify = False)

        zf = zipfile.ZipFile(BytesIO(r.content))

        zf.extractall(path = home )
          
    Scraper()
     
    def extractor():

        os.chdir(r'C:\Users\{}\covid19br-vac-main'.format(user))
        aux2 = os.listdir()

        csvs = []

        for j in aux2:

            if 'processed_' in j:

                csvs.append(j)

        return csvs

    csvs = extractor()

    # Agrega as UFs para ter os dados nacionais

    def concatener():

        def reader(data):
 
            df = pd.read_csv(data).drop(columns = ['city', 'state', 'ibgeID', 'vaccine', 'sex', 'age', 'pop2021'])
      
            return df
        
        dfs = map(lambda uf: reader(uf), csvs)

        consolidado = pd.concat(dfs)

        return consolidado

    data = concatener()

    # Organiza os dados de acordo com a distribuição das doses

    def organizer(data):

        first = data[data['dose'] == 1]

        first = first.groupby('date')[['count']].sum()

        first.columns = ['First dose']

    
        second = data[data['dose'] == 2]

        second = second.groupby('date')[['count']].sum()

        second.columns = ['Second dose']


        third = data[data['dose'] == 3]

        third = third.groupby('date')[['count']].sum()

        third.columns = ['Third dose']
        

        agg = pd.concat([first,second,third],axis = 1)


        return agg

    agg = organizer(data)

    # Realiza a análise desejada

    def analysis(agg):

        pop = 215264280

        aggacum = agg.cumsum()

        final = aggacum/pop

        return final

    final = analysis(agg)
   
    return final

#%%

data = CovidVac()
