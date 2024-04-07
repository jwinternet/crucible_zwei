#!/usr/bin/python3.12
from django import forms

from .models import Locale


class LocaleForm(forms.ModelForm):
    title = forms.CharField(
        label="",
        required=True,
        min_length=4,
        max_length=4,
        widget=forms.TextInput(attrs={'placeholder': 'Locale ID', 'style': 'width: 300px;'}),
    )
    first_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'style': 'width: 300px;'})
    )
    last_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'style': 'width: 300px;'})
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'style': 'width: 300px;'})
    )
    street_address = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Street Address', 'style': 'width: 300px;'})
    )
    city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'City', 'style': 'width: 300px;'})
    )
    state = forms.CharField(
        label="",
        widget=forms.Select(choices=Locale.STATE, attrs={'placeholder': 'State', 'style': 'width: 300px;'}),
    )
    zip_code = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'ZIP Code', 'style': 'width: 300px;'})
    )
    # site_type = forms.CharField(
    #     label="",
    #     required=False,
    #     widget=forms.Select(choices=Site.SITE_TYPES),
    # )
    file_upload = forms.FileField(
        label="Select",
        required=False,
    )

    class Meta:
        model = Locale
        fields = ["title", "first_name", "last_name", "email", "street_address", "city", "state", "zip_code", "file_upload"]


# class FileUploadForm(forms.ModelForm):
#     class Meta:
#         model = Site
#         fields = ["file_upload"]


class PhotoForm(forms.ModelForm):
    front = forms.CharField(
        label="Front",
        required=False,
        widget=forms.Select(choices=Locale.YES_NO_CHOICES),
    )
    back = forms.CharField(
        label="Back",
        required=False,
        widget=forms.Select(choices=Locale.YES_NO_CHOICES),
    )
    left = forms.CharField(
        label="Left",
        required=False,
        widget=forms.Select(choices=Locale.YES_NO_CHOICES),
    )
    right = forms.CharField(
        label="Right",
        required=False,
        widget=forms.Select(choices=Locale.YES_NO_CHOICES),
    )

    class Meta:
        model = Locale
        fields = ["front", "back", "left", "right"]
