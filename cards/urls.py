from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/<int:id>', views.edita, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
]