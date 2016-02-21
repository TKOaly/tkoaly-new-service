from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse

from django_markup import markup

PAGE, DIRECT_LINK = range(2)
FLATPAGE_TYPE_CHOICES = (
    (PAGE, _("Page")),
    (DIRECT_LINK, _("Direct Link")),
)

MARKUP_CHOICES = markup.formatter.choices()


class Flatpage(models.Model):
    menu_category = models.IntegerField(
        choices=settings.FLATPAGES_MENU_CATEGORIES,
        default=settings.FLATPAGES_DEFAULT_MENU_CATEGORY
    )
    menu_index = models.IntegerField(default=0, help_text=_("Menus are sorted ascending by this value. The first menu item in a category is the category link itself. <strong>Note:</strong> The first menu item in the top level category should be the front page."))
    flatpage_type = models.IntegerField(choices=FLATPAGE_TYPE_CHOICES, default=PAGE)
    published = models.BooleanField(default=False, help_text=_("Published pages show up on the menu. Unpublished pages can be reached over direct link."))

    def __unicode__(self):
        return self.localflatpage_set.first().title

class LocalFlatpage(models.Model):
    flatpage = models.ForeignKey(Flatpage)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES)
    url = models.CharField(max_length=100, db_index=True, blank=True)
    title = models.CharField(max_length=100)
    menu_title = models.CharField(
        max_length=40,
        help_text=_("Shorter title that fits in menu elements")
    )
    content = models.TextField(
        help_text=_("Body text for pages, URL for direct links")
    )
    content_markup = models.CharField(
        max_length=20,
        choices=MARKUP_CHOICES,
        default=MARKUP_CHOICES[0][0]
    )

    def __unicode__(self):
        return self.title

    def get_other_lang(self, language):
        return self.flatpage.localflatpage_set.get(language=language)

    def get_absolute_url(self):
        if self.flatpage.flatpage_type == DIRECT_LINK:
            return self.content
        else:
            return reverse('flatpage', kwargs={"url": self.url})


    class Meta:
        unique_together = (('flatpage', 'language'), ('url', 'language'))
        ordering = ('language', 'flatpage__menu_index', 'title')
