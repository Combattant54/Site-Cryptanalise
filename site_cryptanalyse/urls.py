"""
URL configuration for site_cryptanalyse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

import blog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include("blog.urls")),
    path("red/", include("mini_url.urls")),
    path("login/", blog.views.connexion, name="connexion"),
    path("logout/", blog.views.deconnexion, name="deconnexion"),
    path("profile/", blog.views.see_private_profile, name="private_profile"),
    path("profile/<username>/", blog.views.see_profile, name="profile")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)