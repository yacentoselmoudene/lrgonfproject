from django.contrib import admin
from django.urls import path
from website.views import home  # adapte le chemin

urlpatterns = [
    path("", home, name="home"),
]