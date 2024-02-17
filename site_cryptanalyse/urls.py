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
from django.contrib.auth.views import *

import blog
from .views import home_view

urlpatterns = [
    path("", home_view, name="home"),
    path('admin/', admin.site.urls),
    path('blog/', include("blog.urls")),
    path("red/", include("mini_url.urls")),
    path("account/login/", blog.views.connexion, name="connexion"),
    path("account/display/", blog.views.see_private_profile, name="private_profile"),
    path("account/display/<username>/", blog.views.see_profile, name="profile"),
    path("account/logout/", blog.views.deconnexion, name="deconnexion"),
    path("account/signin/", blog.views.create_profile, name="create_user"),
    path("account/change-password/", PasswordChangeView.as_view(), name="confirm_user_creation"),
    path("account/password-changed/", PasswordChangeDoneView.as_view(), name="waiting_account_confirmation"),
    path("account/password-reset/", PasswordResetView.as_view(), name="reset_password"),
    path("account/password-reset/confirm/", PasswordResetConfirmView.as_view(), name="reset_password_confirm"),
    path("account/password-reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("account/password-reset/complete/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_rrot=settings.STATIC_ROOT)