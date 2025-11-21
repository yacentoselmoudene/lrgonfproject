from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from website.views import home, usedLang
from django.contrib.auth import views as auth_views
from website.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('website.urls')),
    # Auth
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # i18n (changement de langue)
    path("lang/", switch_language, name="switch_language"),
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)