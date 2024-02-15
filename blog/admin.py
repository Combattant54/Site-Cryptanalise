from django.contrib import admin
from .models import Article, Categorie

class AdminArticle(admin.ModelAdmin):
    list_display = ("title", "autor", "date_creation", "date_modification")
    list_filter = ("categories", "autor")
    date_hierarchy = "date_creation"
    ordering = ("date_modification", )
    search_fields = ("title", "content")
    
    fieldsets = (
        ("General", {
            "classes": ["collapse"],
            "fields": ("title", "slug", "autor", "categories"  ),
        }),
        ("Corps de l'article", {
            "description": "Le corps de l'article avec des balises html",
            "fields":("content",)
        })
    )
    prepopulated_fields = {"slug": ("title", )}


# Register your models here.
admin.site.register(Article, AdminArticle)
admin.site.register(Categorie)