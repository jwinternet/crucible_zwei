#!/usr/bin/python3.12
from django.contrib import admin

from .models import Locale, Comment


@admin.register(Locale)
class LocaleAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "date_added", "updated")
    list_filter = ["owner", "date_added", "updated"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["owner"]
    date_hierarchy = "updated"
    ordering = ["updated"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'locale', 'created']
    list_filter = ['created', 'updated']
    search_fields = ['name', 'email', 'body']
