from django.contrib import admin
from django.urls import path
from website.views import *  # adapte le chemin

urlpatterns = [
    path("", home, name="home"),
    path('changelang/', changeSitegeLang, name='changeSitegeLang'),
]