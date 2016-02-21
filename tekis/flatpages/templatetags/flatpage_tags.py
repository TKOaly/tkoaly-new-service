from django import template
from django.utils.translation import get_language

from tekis.flatpages.models import LocalFlatpage, Sponsor, PAGE

register = template.Library()


@register.inclusion_tag("flatpages/menu.html")
def menu_for_category(category_id):
    """Render a `<li>` menu for the given category. This will drop the first
    item, which you can get a link to with the other tag,
    `mainpage_link_for_category`. This avoids redundancy.

    The category ID must match with a category defined in
    settings.FLATPAGES_MENU_CATEGORIES.

    """
    pages = LocalFlatpage.objects.filter(
        flatpage__published=True,
        flatpage__menu_category=category_id,
        language=get_language()
    )
    return {"pages": pages}

@register.simple_tag
def mainpage_link_for_category(category_id):
    """Render the URL to the main page for given category ID.

    The category ID must match with a category defined in
    settings.FLATPAGES_MENU_CATEGORIES.

    """
    page = LocalFlatpage.objects.filter(
        flatpage__published=True,
        flatpage__menu_category=category_id,
        language=get_language()
    ).first()
    if page:
        return page.get_absolute_url()
    else:
        return "#no_page"

@register.inclusion_tag("flatpages/sponsors.html")
def show_sponsors():
    return {"sponsors": Sponsor.objects.filter(is_active=True)}

@register.inclusion_tag("flatpage_embed.html")
def embed_flatpage(url):
    lang = get_language()

    try:
        page = LocalFlatpage.objects.get(
            url=url,
            language=lang,
            flatpage__flatpage_type=PAGE
        )
    except LocalFlatpage.DoesNotExist:
        # check if this page url exists in some other language
        pages = LocalFlatpage.objects.filter(
            url=url,
            flatpage__flatpage_type=PAGE
        )
        if pages:
            # it does
            page = pages.first()
            try:
                page = page.get_other_lang(lang)
            except LocalFlatpage.DoesNotExist:
                # use the content from the other language instead
                pass
        else:
            # no such page whatsoever
            return {}
    return {"page": page}
