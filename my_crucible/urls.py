#!/usr/bin/python3.12
"""Defines URL patterns for locales."""
from django.urls import path

from . import views


app_name = "my_crucible"
urlpatterns = [
    # Home page
    path("", views.index, name="index"),
    # Page that shows all locales.
    path("locales/", views.locales, name="locales"),
    path("useful_links/", views.useful_links, name="useful_links"),
    path("documentation/", views.documentation, name="documentation"),
    path("contacts/", views.contacts, name="contacts"),
    path("about/", views.about, name="about"),
    # Detail page for a single locale.
    path("locales/<slug:locale_id>/", views.locale, name="locale"),
    # Page for adding a new locale.
    path("new_locale/", views.new_locale, name="new_locale"),
    # Page for editing a locale.
    path("edit_locale/<int:locale_id>/", views.edit_locale, name="edit_locale"),
    path("photo_checklist/<int:locale_id>/", views.photo_checklist, name="photo_checklist"),
    path('export_all_locales/', views.export_all_locales, name='export_all_locales'),
    path('export_locale/<int:locale_id>/', views.export_locale, name='export_locale'),
    path('download_file/<int:locale_id>/', views.download_file, name='download_file'),
    path('search_results/', views.SearchResultsView.as_view(), name='search_results'),
    path('<int:locale_id>/comment/', views.locale_comment, name='locale_comment'),
]
