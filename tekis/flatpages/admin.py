from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext as _

from tekis.flatpages import models


class LocalFlatpageInline(admin.StackedInline):
    model = models.LocalFlatpage
    extra = max_num = len(settings.LANGUAGES)

    prepopulated_fields = {
        "url": ("title",),
    }
    fieldsets = (
        (None, {
            'fields': ("language", "title", "content")
        }),
        (_("Advanced options"), {
            'fields': ("menu_title", "url", "content_markup"),
            'classes': ("collapse",)
        }),
    )

    def get_formset(self, request, obj=None, **kwargs):
        """returns a custom formset subclass that sets initial data for each
        language page
        """
        formset_class = super(LocalFlatpageInline, self).get_formset(
            request, obj, **kwargs
        )

        if obj:
            return formset_class
        else:
            class LanguageDefaultsFormset(formset_class):
                def get_form_kwargs(self, index):
                    kwargs = super(LanguageDefaultsFormset, self).get_form_kwargs(index)
                    if index is not None:
                        try:
                            lang = settings.LANGUAGES[index][0]
                            kwargs.update({"initial": {"language": lang}})
                        except IndexError:
                            pass

                    return kwargs

            return LanguageDefaultsFormset


class FlatpageAdmin(admin.ModelAdmin):
    inlines = [
        LocalFlatpageInline
    ]
    list_display = ['__unicode__', 'menu_category',
                    'flatpage_type', 'published',
                    'available_languages']

    def available_languages(self, obj):
        return ",".join(obj.localflatpage_set.values_list("language", flat=True))
    available_languages.short_description = _("Available languages")


class SponsorAdmin(admin.ModelAdmin):
    pass

class ContentImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Flatpage, FlatpageAdmin)
admin.site.register(models.Sponsor, SponsorAdmin)
admin.site.register(models.ContentImage, ContentImageAdmin)
