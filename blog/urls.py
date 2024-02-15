from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("article/", views.show_recent_articles),
    path("article/<int:id>/", views.show_article, name="blog.views.article"),
    path("article/<int:id>/<str:slug>", views.show_article, name="blog.views.article"),
    path("article/<int:year>/<int:month>/", views.search_date_articles),
    path("contact/", views.contact, name="blog.views.contact"),
]
