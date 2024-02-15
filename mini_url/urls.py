from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.get_url_form, name="mini_url.create_url"),
    path("lk/<url_code>/", views.redirect_short, name="mini_url.redirect"),
    path("show/", views.show_redirects, name="mini_url.show"),
]