from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from website.views import home
from django.contrib.auth import views as auth_views
from website.views import home, switch_language

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),


    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # i18n (changement de langue)
    path("lang/", switch_language, name="switch_language"),
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)