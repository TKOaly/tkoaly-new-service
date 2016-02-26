from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext as _


class FlatpagesConfig(AppConfig):
    name = 'flatpages'
    verbose_name = _('Flatpages')
