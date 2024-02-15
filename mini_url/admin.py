from django.contrib import admin
from .models import MiniURL

# Register your models here.
class AdminMiniURL(admin.ModelAdmin):
    list_display = ("long_url", "url_code", "creation_date", "creator", "access_amount")
    list_filter = ("creator", )
    date_hierarchy = "creation_date"
    ordering = ("creation_date", )
    search_fields = ("long_url", )
    
    fields = ("long_url", "creator")

admin.site.register(MiniURL, AdminMiniURL)