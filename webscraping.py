from base64 import encode
from re import A
#from matplotlib import image
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
#import bs4
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
#import time


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
    #lista_imagem=[]
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
        #imagem = ap.find('img', class_="realtyCardImagesstyle__ImageRealty-sc-11vdyejw-0 dfIThs").img
        #imagem.get('src')

        #lista_imagem.append(imagem)
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
                   'Preco':lista_aluguel_total
                  })
        
    return df
def mudar_data_to_json(df):
    return df.to_json(orient='records') 
def run(num_paginas,ap):
    pegar_paginas(num_paginas,ap)
    lista=pegar_apartamentos(num_paginas,ap)
    return eval(mudar_data_to_json(data(lista)))
def dataframe(num_paginas, ap):
    pegar_paginas(num_paginas,ap)
    lista=pegar_apartamentos(num_paginas,ap)
    dados = data(lista)
    lista_bairros = dados['Bairro'].unique()
    return lista_bairros
def bairros_baratos(df):
    df1 = df.groupby(['Bairro']).agg({'Preco': 'mean'}).reset_index()
    precos_mais_baratos = list(df1.sort_values(by='Preco',ascending=True).head(5)['Preco'])
    bairros_mais_baratos = list(df1.sort_values(by='Preco',ascending=True).head(5)['Bairro']) 
    return bairros_mais_baratos, precos_mais_baratos
def plota_bairros_baratos(bairros_mais_baratos,precos_mais_baratos):
    plt.figure(figsize=(9,6))
    parameters = {'axes.labelsize': 10,
            'axes.titlesize': 15}
    plt.rcParams.update(parameters)
    plt.ylim(0,400000)
    plt.title('Média dos Alugueis de Bairros mais baratos de São Paulo')
    plt.bar(bairros_mais_baratos,precos_mais_baratos, color='#3957bd')
    plt.xlabel('Bairros')
    plt.ylabel('Preços')
    plt.savefig('C:\\Users\\ricar\\OneDrive - Insper - Institudo de Ensino e Pesquisa\\Quarto Semestre\\TECWEB\\PROJETO3\\projeto-3-tiringa_serra_talhada\\cards\\static\\cards\\img\\ala.png')

def plota_area_versus_preco(df):
    plt.figure(figsize=(9,6))
    parameters = {'axes.labelsize': 10,
            'axes.titlesize': 15}
    plt.rcParams.update(parameters)
    plt.title('Correlação entre Área vs Preços')
    plt.scatter(df['Preco'],df['Area'], color='#3957bd')
    plt.xlabel('Preço')
    plt.ylabel('Área')
    plt.savefig('C:\\Users\\ricar\\OneDrive - Insper - Institudo de Ensino e Pesquisa\\Quarto Semestre\\TECWEB\\PROJETO3\\projeto-3-tiringa_serra_talhada\\cards\\static\\cards\\img\\ala2.png')
    

lista_imoveis=run(30,'card-body')
lista_bairros = dataframe(30,'card-body')

