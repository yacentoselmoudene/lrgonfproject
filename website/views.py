from django.shortcuts import render

from django.shortcuts import render, redirect
from django.urls import reverse

SUPPORTED_LANGS = ("fr", "en", "ar")


def get_lang(request):
    lang = request.session.get("lang", "fr")
    if lang not in SUPPORTED_LANGS:
        lang = "fr"
    return lang


def home(request):
    lang = get_lang(request)
    template_name = f"home_{lang}.html"
    return render(request, template_name, {"lang": lang})


def switch_language(request):
    if request.method == "POST":
        lang = request.POST.get("lang")
        if lang in SUPPORTED_LANGS:
            request.session["lang"] = lang
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or reverse("home")
    return redirect(next_url)
