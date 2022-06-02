from django.shortcuts import render, redirect
from .models import Card
from webscraping import *

pegar_paginas(4,'card-body')
lista=pegar_apartamentos(4,'card-body')
dados = data(lista)
bairros_mais_baratos, precos_mais_baratos = bairros_baratos(dados)
plota_bairros_baratos(bairros_mais_baratos,precos_mais_baratos)
plota_area_versus_preco(dados)
def index(request):
    if request.method == 'POST':
        
        card=Card()
        title=request.POST.get('title')
        #content=request.POST.get('content')
        card.title=title
        #card.content=content
        card.save()
        return redirect('index')
    else:
        return render(request, 'cards/index.html', {'cards': lista_bairros})
        
def imoveis(request):
    salvaImoveis()
    title=request.POST.get('bairro')
    #content=request.POST.get('content')
    print(title)
    apartamentos = Card.objects.filter(bairro = title)
    # card=Card()
    # card.title=title
    # card.content=content
    # card.save()
    return render(request, 'cards/imoveis.html', {'cards': apartamentos})
        

def delete(request, id):
    card=Card.objects.get(id=id)
    card.delete()
    return redirect('index')

def edita(request,id):    
    Card.objects.filter(id=id).update(title=request.POST.get('title'), content=request.POST.get('content'))
    return redirect('index')

########################## ADNEY
def pegaImoveis():
    # faz scarpping
    return lista_imoveis

def salvaImoveis():
    imoveis = pegaImoveis()
    for imovel in imoveis:
        rua = imovel['Rua']
        bairro = imovel['Bairro']
        quartos = imovel['Quartos']
        vagas = imovel['Vagas']
        banheiros = imovel['Banheiros']
        preco = imovel['Preco']
        card = Card(rua = rua, bairro= bairro, quartos=quartos, vagas=vagas, banheiros=banheiros, preco=preco)
        card.save()

def bairroSelecionado(request):
    bairro = request.POST.get('bairro')
    apartamentos = []
    for imovel in lista_imoveis:
        print(imovel['Bairro'])
        if imovel['Bairro'] == bairro:
            apartamentos.append(imovel)
    return render(request, 'cards/imoveis.html', {'cards': apartamentos})




