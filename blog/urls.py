from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("article/", views.show_recent_articles, name="blog.views.accueil"),
    path("article/<int:id>/", views.show_article, name="blog.views.article"),
    path("article/<int:id>/<str:slug>", views.show_article, name="blog.views.article"),
    path("article/<int:year>/<int:month>", views.search_date_articles),
    path("contact/", views.contact, name="blog.views.contact"),
    path("category/<int:id>/", views.get_articles_from_category, name="blog.views.category"),
    path("category/<int:id>/<str:slug>", views.get_articles_from_category, name="blog.views.category"),
]
