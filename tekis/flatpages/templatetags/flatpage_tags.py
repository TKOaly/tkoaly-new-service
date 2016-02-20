from django import template
from django.utils.translation import get_language

from tekis.flatpages.models import LocalFlatpage

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
