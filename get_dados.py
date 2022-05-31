
from base64 import encode
from re import A
from matplotlib import image
# import seaborn as sns
# import matplotlib as plt
# import numpy as np
# from numpy import arange
import pandas as pd
# from random import randint
# Remove warnings
import warnings
warnings.filterwarnings('ignore')
# from IPython.display import display, HTML  # Para ter melhor print.
from math import *
# para nos comunicarmos com a Web
import requests
# para extrair informações de páginas HTML
import bs4
from bs4 import BeautifulSoup
import time


#pega todas as páginas
def pegar_paginas(num_paginas,ap):
    headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    lista_total = []
    for pagina in range(1,num_paginas):
        url = 'https://www.lelloimoveis.com.br/venda/residencial/{}-pagina/'.format(pagina)
        resposta = requests.get(url = url, headers=headers)
        resposta.encoding=='utf-8'
        soup = BeautifulSoup(resposta.content, 'html.parser')
        lista_aps = soup.find_all(class_=ap, limit=12)
        lista_total.append(lista_aps)
    return lista_total
#pega todos os apartamentos
def pegar_apartamentos(num_paginas,ap):
    lista_paginas=pegar_paginas(num_paginas,ap)
    apartamento=[]
    for pagina in lista_paginas:
        for item in pagina:
            apartamento.append(item)
    return apartamento
#criar dataframe
def data(lista):
    #listas necessárias
    lista_tipo=[]
   
    lista_rua=[]
    lista_bairro=[]
    lista_area=[]
    lista_quartos=[]
    lista_vagas=[]
    lista_banheiros=[]
    lista_aluguel_total=[]
    


    for i in range(0, len(lista)):
        ap = lista[i] #procura cada lista de apartamentos
        #tipo do ap
       
        #tipo do ap
        tipo=ap.find('div',attrs={'class': "card-title h5"}).text
        lista_tipo.append(tipo)
        #rua
        rua=ap.find('p',attrs={'class': "text-truncate mb-0"}).text
        lista_rua.append(rua)
        #bairro
        bairro=ap.find('span',attrs={'class': "card-text-neighborhood mt-1 text-truncate"}).text.split(',')[0]
        lista_bairro.append(bairro)
        #area do ap
        area=ap.find('span',attrs={'class': "tagItemstyle__TagValue-sc-13sggff-3 edPntf"})
        if area==None:
            area=0
        else:
            area=int(ap.find('span',attrs={'class': "tagItemstyle__TagValue-sc-13sggff-3 edPntf"}).text.split("m²")[0])
        lista_area.append(area)
        
        #numero de quartos
        quartos=ap.find('span',attrs={'class': "tagItemstyle__ComplementValue-sc-13sggff-4 hERajv ml-0"})
        if quartos==None:
            quartos=0            
        else:
            quartos=int(ap.find('span',attrs={'class': "tagItemstyle__ComplementValue-sc-13sggff-4 hERajv ml-0"}).text.split(" ")[0])
        lista_quartos.append(quartos)
        #numero de vagas de carro
        vagas_carro=ap.find('span',attrs={'data-testid': "realty-parking-lot-quantity"})
        if vagas_carro==None:
            vagas_carro=0
        else:
            vagas_carro=int(ap.find('span',attrs={'data-testid': "realty-parking-lot-quantity"}).text.split("Garagens")[0])
        lista_vagas.append(vagas_carro)
        
        #numero de banheiros
        banheiros=ap.find('span',attrs={'data-testid':"realty-bathroom-quantity"})
        if banheiros==None:
            banheiros=0
        else:                
            banheiros=int(ap.find('span',attrs={'data-testid':"realty-bathroom-quantity"}).text.split("Banheiros")[0])
        lista_banheiros.append(banheiros)
        #valor do aluguel
        aluguel=ap.find('p',attrs={'class':"mb-0 font-weight-bold"})
        if aluguel==None:
            aluguel=0
        else:
            aluguel=int(ap.find('p',attrs={'class':"mb-0 font-weight-bold"}).text.split("R$")[1].replace(",",""))
        lista_aluguel_total.append(aluguel)
    
    df = pd.DataFrame({'Tipo': lista_tipo,
                   
                   'Rua': lista_rua,
                   'Bairro': lista_bairro,
                   'Area': lista_area,
                   'Quartos':lista_quartos,
                    'Vagas':lista_vagas,
                    'Banheiros':lista_banheiros,
                   'Preço de Venda':lista_aluguel_total
                  })
        
    return df
def mudar_data_to_json(df):
    return df.to_json(orient='records') 
def run(num_paginas,ap):
    pegar_paginas(num_paginas,ap)
    lista=pegar_apartamentos(num_paginas,ap)
    print(mudar_data_to_json(data(lista)))
list_dict=run(4,'card-body')


