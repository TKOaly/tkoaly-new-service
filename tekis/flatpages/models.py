from __future__ import unicode_literals

import os.path

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django_markup import markup

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
from easy_thumbnails.fields import ThumbnailerImageField


PAGE, DIRECT_LINK, PAGE_SEPARATOR, LINK_SEPARATOR = range(4)
# Separator page types disabled for now because the retro template
# doesn't support them

FLATPAGE_TYPE_CHOICES = (
    (PAGE, _("Page")),
#    (PAGE_SEPARATOR, _("Page with menu separator")),
    (DIRECT_LINK, _("Direct Link")),
#    (LINK_SEPARATOR, _("Direct Link with menu separator"))
)

MARKUP_CHOICES = markup.formatter.choices()

MENU_CATEGORIES = [(k, _(v)) for k,v in settings.FLATPAGES_MENU_CATEGORIES]

class Flatpage(models.Model):
    menu_category = models.IntegerField(
        choices=MENU_CATEGORIES,
        default=settings.FLATPAGES_DEFAULT_MENU_CATEGORY,
        verbose_name=_("Menu category")
    )
    menu_index = models.IntegerField(
        default=0,
        help_text=_("Menus are sorted ascending by this value. The first menu item in a category is the category link itself. <strong>Note:</strong> The first menu item in the top level category should be the front page."),
        verbose_name=_("Menu index")
    )
    flatpage_type = models.IntegerField(
        choices=FLATPAGE_TYPE_CHOICES,
        default=PAGE,
        verbose_name=_("Flatpage type")
    )
    published = models.BooleanField(
        default=False,
        help_text=_("Published pages show up on the menu. Unpublished pages can be reached over direct link."),
        verbose_name=_("Published")
    )

    def __unicode__(self):
        try:
            return self.localflatpage_set.first().title
        except AttributeError:
            return unicode(_("(no content yet)"))

    class Meta:
        verbose_name = _("Flatpage")
        verbose_name_plural = _("Flatpages")

class LocalFlatpage(models.Model):
    flatpage = models.ForeignKey(Flatpage)
    language = models.CharField(
        max_length=5,
        choices=settings.LANGUAGES,
        verbose_name=_("Language")
    )
    url = models.CharField(
        max_length=100,
        db_index=True,
        blank=True,
        verbose_name=_("URL"),
        help_text=_("The page is accessible on this path. Even external links have one.")
    )
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    menu_title = models.CharField(
        max_length=40,
        blank=True,
        verbose_name=_("Menu Title"),
        help_text=_("Shorter title that fits in menu elements")
    )
    content = models.TextField(
        verbose_name=_("Content"),
        help_text=_("Body text for pages, URL for direct links")
    )
    content_markup = models.CharField(
        verbose_name=_("Content markup"),
        max_length=20,
        choices=MARKUP_CHOICES,
        default=MARKUP_CHOICES[0][0]
    )

    def has_separator(self):
        return self.flatpage.flatpage_type in (PAGE_SEPARATOR, LINK_SEPARATOR)

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
        verbose_name = _("Local Flatpage")
        verbose_name_plural = _("Local Flatpages")
        unique_together = (('flatpage', 'language'), ('url', 'language'))
        ordering = ('language', 'flatpage__menu_index', 'title')


class Sponsor(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name")
    )
    url = models.URLField(verbose_name=_("URL"))
    logo = models.ImageField(upload_to="sponsors/")
    titletext = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Title text")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")
        ordering = ('name',)


def namefromfile(fieldfile):
    "directories/<FILENAME>.ext -> <FILENAME>"

    filename = fieldfile.name
    _path, filename = os.path.split(filename)
    filename, _ext = os.path.splitext(filename)

    return filename


class ContentImage(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        blank=True
    )
    image = ThumbnailerImageField(
        upload_to='content_images/',
        blank=True,
        verbose_name=_("Image")
    )

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.name:
            self.name = namefromfile(self.image)

        super(ContentImage, self).save(**kwargs)

    def get_thumbnail_list(self):
        ret = []
        for alias_name, alias_opts in settings.THUMBNAIL_ALIASES[""].iteritems():
            thumbinfo = {
                "name": _(alias_name),
                "url": self.image[alias_name].url,
            }

            if "size" in alias_opts:
                thumbinfo.update({
                    "size_x": alias_opts["size"][0],
                    "size_y": alias_opts["size"][1],
                })

            ret.append(thumbinfo)
        return ret


    class Meta:
        verbose_name = _("content image")
        verbose_name_plural = _("content images")
        ordering = ('name',)


class Download(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        blank=True
    )
    size = models.IntegerField(
        editable=False,
        verbose_name=_("Size")
    )
    uploaded_file = models.FileField(
        upload_to="download/",
        verbose_name=_("File")
    )

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.name:
            self.name = namefromfile(self.uploaded_file)
        if not self.size:
            self.size = self.uploaded_file.size

        super(Download, self).save(**kwargs)

    class Meta:
        verbose_name = _("download")
        verbose_name_plural = _("downloads")
        ordering = ('name',)

saved_file.connect(generate_aliases_global)
