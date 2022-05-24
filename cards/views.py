from django.shortcuts import render, redirect
from .models import Card


def index(request):
    if request.method == 'POST':
        card=Card()
        title=request.POST.get('title')
        content=request.POST.get('content')
        card.title=title
        card.content=content
        card.save()
        return redirect('index')
    else:
        allCards = Card.objects.all()
        return render(request, 'cards/index.html', {'cards': allCards})

def delete(request, id):
    card=Card.objects.get(id=id)
    card.delete()
    return redirect('index')

def edita(request,id):    
    Card.objects.filter(id=id).update(title=request.POST.get('title'), content=request.POST.get('content'))
    return redirect('index')
