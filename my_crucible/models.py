#!/usr/bin/python3.12
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager


class Locale(models.Model):
    """A specific location."""

    # General Locale Information
    title = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.SlugField(max_length=250)
    date_added = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    STATE = [
        (None, "State"),
        ("AK", "Alaska"),
        ("AL", "Alabama"),
        ("AR", "Arkansas"),
        ("AZ", "Arizona"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("DC", "District of Columbia"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("IA", "Iowa"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("MA", "Massachusetts"),
        ("MD", "Maryland"),
        ("ME", "Maine"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MO", "Missouri"),
        ("MS", "Mississippi"),
        ("MT", "Montana"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("NE", "Nebraska"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NV", "Nevada"),
        ("NY", "New York"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("PR", "Puerto Rico"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VA", "Virginia"),
        ("VT", "Vermont"),
        ("WA", "Washington"),
        ("WI", "Wisconsin"),
        ("WV", "West Virginia"),
        ("WY", "Wyoming"),
    ]
    state = models.CharField(
        choices=STATE,
        max_length=2
    )
    zip_code = models.CharField(max_length=5)
    # SITE_TYPES = [
    #     (None, "Site Type"),
    #     ("Wawa", "Wawa"),
    #     ("Sheetz", "Sheetz"),
    #     ("Thorntons", "Thorntons"),
    #     ("AT&T", "AT&T"),
    #     ("Verizon", "Verizon")
    # ]
    # site_type = models.CharField(
    #     choices=SITE_TYPES,
    #     max_length=25
    # )
    YES_NO_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No")
    ]

    # Photo Information
    front = models.CharField(
        choices=YES_NO_CHOICES,
        default="No",
        max_length=4,
    )
    back = models.CharField(
        choices=YES_NO_CHOICES,
        default="No",
        max_length=4,
    )
    left = models.CharField(
        choices=YES_NO_CHOICES,
        default="No",
        max_length=4,
    )
    right = models.CharField(
        choices=YES_NO_CHOICES,
        default="No",
        max_length=4,
    )

    file_upload = models.FileField(
        upload_to='my_crucible/media/%Y/%m/%d/',
        blank=True
    )

    tags = TaggableManager()

    class Meta:
        ordering = ['title']

    def __str__(self):
        """Return a string representation of the model."""
        return self.title

    def get_absolute_url(self):
        return reverse(
            "my_crucible:locale",
            args=[self.slug]
        )

    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(self.title)

        super(Locale, self).save(*args, **kwargs)


class Comment(models.Model):
    locale = models.ForeignKey(
        Locale,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.locale}'
