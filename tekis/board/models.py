from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models


VERBOSE_NAME = _('Board')


class Board(models.Model):
    year = models.IntegerField()

    officers = models.TextField()

    class Meta:
        ordering = ("year",)
        get_latest_by = "year"
        verbose_name = _("Board")
        verbose_name_plural = _("Boards")

    def __unicode__(self):
        return _("Board %(year)s") % {"year": self.year}

ROLE_CHOICES = (
    (0, _("Chairman")),
    (1, _("Treasurer")),
    (2, _("Secretary")),
    (3, _("Vice chairman")),
    (4, _("Board Member")),
    (5, _("Study affairs")),
    (6, _("Communications")),
    (7, _("Corporate affairs")),
    (8, _("RV affairs")),
    (9, _("Freshman affairs")),
    (20, _("First deputy board member")),
    (21, _("Second deputy board member")),
    (22, _("Third deputy board member")),
    (23, _("Fourth deputy board member")),
)


class BoardMember(models.Model):
    board = models.ForeignKey(Board)
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    face = models.ImageField(upload_to="board_faces/%Y/", verbose_name=_("Mugshot"))
    role = models.IntegerField(choices=ROLE_CHOICES, verbose_name=_("Role"))
    contact = models.CharField(max_length=100, default=_("firstname.lastname(at)cs.helsinki.fi"), verbose_name=_("Contact"))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ("role",)
        verbose_name = _("Board Member")
        verbose_name_plural = _("Board Members")
