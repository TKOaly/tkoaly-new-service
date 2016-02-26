from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext as _


class BoardConfig(AppConfig):
    name = 'board'
    verbose_name = _('Board')
