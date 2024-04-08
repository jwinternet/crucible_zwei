#!/usr/bin/python3.12
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q
from django.views.decorators.http import require_POST

from csv import writer

from .models import Locale, Comment
from .forms import LocaleForm, PhotoForm, CommentForm


def index(request):
    """The home page for My Crucible."""
    return render(request, "my_crucible/index.html")


@login_required
def locales(request):
    """Show all locales."""
    locales = Locale.objects.order_by("title")
    count = locales.count()

    # Pagination with 3 posts per page
    paginator = Paginator(locales, 10)
    page_number = request.GET.get("page", 1)
    try:
        locale = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        locale = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        locale = paginator.page(paginator.num_pages)
    context = {"locales": locale, "count": count}
    return render(request, "my_crucible/locales.html", context)


@login_required
def locale(request, locale_id):
    """Show a single locale and all of its notes."""
    try:
        # site = Site.objects.get(id=site_id)
        locale = get_object_or_404(Locale, slug=locale_id)
        # # Make sure the locale belongs to the current user.
        # if site.owner != request.user:
        #     raise Http404
        comments = locale.comments.all()
        form = CommentForm()
        context = {
            "locale": locale, "comments": comments, "form": form
        }
        return render(request, "my_crucible/locale.html", context)

    except:
        return redirect("my_crucible:locales")


@login_required
def new_locale(request):
    """Add a new locale."""
    if request.method != "POST":
        # No data submitted; create a blank form.
        locale_form = LocaleForm()
    else:
        # POST data submitted; process data.
        locale_form = LocaleForm(request.POST, request.FILES)
        if locale_form.is_valid():
            new_locale = locale_form.save(commit=False)
            new_locale.owner = request.user
            new_locale.save()
            return redirect("my_crucible:locales")

    # Display a blank or invalid form.
    context = {"locale_form": locale_form}
    return render(request, "my_crucible/new_locale.html", context)


@login_required
def edit_locale(request, locale_id):
    """Edit an existing locale."""
    locale = get_object_or_404(Locale, id=locale_id)

    if request.method != "POST":
        # No data submitted; create a blank form.
        locale_form = LocaleForm(instance=locale)

    else:
        # POST data submitted; process data.
        locale_form = LocaleForm(instance=locale, data=request.POST, files=request.FILES)
        if locale_form.is_valid():
            locale_form.save()
            context = {"locale": locale}
            return render(request, "my_crucible/locale.html", context)

    # Display a blank or invalid form.
    context = {"locale": locale, "locale_form": locale_form}
    return render(request, "my_crucible/edit_locale.html", context)


@login_required
def photo_checklist(request, locale_id):
    """Edit an existing locale."""
    locale = get_object_or_404(Locale, id=locale_id)

    if request.method != "POST":
        # No data submitted; create a blank form.
        photo_form = PhotoForm(instance=locale)

    else:
        # POST data submitted; process data.
        photo_form = PhotoForm(instance=locale, data=request.POST, files=request.FILES)
        if photo_form.is_valid():
            photo_form.save()
            context = {"locale": locale}
            return render(request, "my_crucible/locale.html", context)

    # Display a blank or invalid form.
    context = {"locale": locale, "photo_form": photo_form}
    return render(request, "my_crucible/photo_checklist.html", context)


@login_required
def export_all_locales(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export_all_locales.csv"'
    export_locales = Locale.objects.all()

    my_writer = writer(response)
    my_writer.writerow([
        "title", "first_name", "last_name", "email", "street_address", "city", "state", "zip_code", "front", "back",
        "left", "right",
    ])

    for export_locale in export_locales:
        my_writer.writerow([
            export_locale.title,
            export_locale.first_name,
            export_locale.last_name,
            export_locale.email,
            export_locale.street_address,
            export_locale.city,
            export_locale.state,
            export_locale.zip_code,
            export_locale.front,
            export_locale.back,
            export_locale.left,
            export_locale.right,
        ])
    return response


@login_required
def export_locale(request, locale_id):
    export_locale = get_object_or_404(Locale, id=locale_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="export_locale_{export_locale.title}.csv"'

    my_writer = writer(response)
    my_writer.writerow([
        "title", "first_name", "last_name", "email", "street_address", "city", "state", "zip_code", "front", "back",
        "left", "right",
    ])
    my_writer.writerow([
        export_locale.title,
        export_locale.first_name,
        export_locale.last_name,
        export_locale.email,
        export_locale.street_address,
        export_locale.city,
        export_locale.state,
        export_locale.zip_code,
        export_locale.front,
        export_locale.back,
        export_locale.left,
        export_locale.right,
    ])
    return response


@login_required
def download_file(request, locale_id):
    locale = get_object_or_404(Locale, id=locale_id)
    return FileResponse(locale.file_upload.open(), as_attachment=True,)


@login_required
def useful_links(request):
    return render(request, "my_crucible/useful_links.html")


@login_required
def documentation(request):
    return render(request, "my_crucible/documentation.html")


@login_required
def contacts(request):
    return render(request, "my_crucible/contacts.html")


@login_required
def about(request):
    return render(request, "my_crucible/about.html")


class SearchResultsView(ListView):
    model = Locale
    template_name = "my_crucible/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Locale.objects.filter(
            Q(title__icontains=query)
        )
        return object_list


@require_POST
def locale_comment(request, locale_id):
    """Edit an existing locale."""
    locale = get_object_or_404(Locale, id=locale_id)
    comment = None

    # POST data submitted; process data.
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.locale = locale
        comment.save()

    # Display a blank or invalid form.
    context = {"locale": locale, "form": form, "comment": comment}
    return render(request, "my_crucible/comment.html", context)
