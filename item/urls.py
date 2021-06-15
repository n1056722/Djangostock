"""stock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from item import views

app_name = 'item'
urlpatterns = [
    path('api/list/', views.ItemListView.as_view(), name='api_list'),
    path('api/<slug:pk>/detail/', views.ItemRetrieveView.as_view(), name='api_detail'),

    path('list/', views.list, name='list'),
    path('add/', views.add, name='add'),
    path('<slug:pk>/edit/', views.edit, name='edit'),
    path('<slug:pk>/delete/', views.delete, name='delete'),
    path('home/', views.home, name='home'),

]
