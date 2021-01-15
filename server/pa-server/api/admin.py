from django.contrib import admin
from .models import MarkPatentInfo, DesignPatentInfo


@admin.register(MarkPatentInfo)
class MarkPatentInfoAdmin(admin.ModelAdmin):
    list_display = ('app_num', 'category')
    list_filter = ('category',)
    search_fields = ('app_num',)


@admin.register(DesignPatentInfo)
class DesignPatentInfoAdmin(admin.ModelAdmin):
    list_display = ('app_num', 'category')
    list_filter = ('category',)
    search_fields = ('app_num',)