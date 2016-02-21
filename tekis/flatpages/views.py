from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import get_language
from django import http

from tekis.flatpages.models import LocalFlatpage, PAGE, PAGE_SEPARATOR


def flatpage(request, url):
    lang = get_language()

    try:
        page = LocalFlatpage.objects.get(
            url=url,
            language=lang,
            flatpage__flatpage_type__in=(PAGE, PAGE_SEPARATOR)
        )
    except LocalFlatpage.DoesNotExist:
        # check if this page url exists in some other language
        pages = LocalFlatpage.objects.filter(
            url=url,
            flatpage__flatpage_type__in=(PAGE, PAGE_SEPARATOR)
        )
        if pages:
            # it does
            page = pages.first()
            try:
                right_page = page.get_other_lang(lang)
                return redirect(right_page.get_absolute_url())
            except LocalFlatpage.DoesNotExist:
                # use the content from the other language instead
                pass
        else:
            # no such page whatsoever
            raise http.Http404("No such flatpage: lang=%r, url=%r" % (lang,url))

    return render(request, "flatpage.html", context={"page":page})
