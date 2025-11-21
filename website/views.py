from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import updateSitegeLangModel

SUPPORTED_LANGS = ("fr", "en", "ar")
usedLang = 'ar'

def get_lang(request):
    lang = request.session.get("lang", "fr")
    if lang not in SUPPORTED_LANGS:
        lang = "fr"
    return lang


def home(request):
    lang = get_lang(request)
    template_name = f"home.html"
    #template_name = f"home_{lang}.html"
    latest_news = [{"id":1, "title":"Bienvenue sur notre site", "content":"Ceci est la page d'accueil."}]
    print(usedLang)
    return render(request, template_name, {"usedLang": usedLang, "news":latest_news})


def switch_language(request):
    if request.method == "POST":
        lang = request.POST.get("lang")
        if lang in SUPPORTED_LANGS:
            request.session["lang"] = lang
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or reverse("home")
    return redirect(next_url)


def updateSitegeLang(lang):
    global usedLang
    usedLang = lang

def changeSitegeLang(request):
    global usedLang
    lang = request.POST.get('lang')
    link = request.POST.get('link')
    usedLang = str(lang)
    updateSitegeLang(str(lang))
    updateSitegeLangModel(str(lang))
    return JsonResponse({'lang': usedLang})