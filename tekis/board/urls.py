from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from tekis.board.views import board
from tekis.flatpages.views import flatpage

urlpatterns = [
    url(r"^$", board, name="board"),
    url(r"^(?P<year>\d{4})/$", board, name="board"),
    url(r"^%s/$" % _("older"), flatpage,
        name="legacy-boards", kwargs={"url": "legacy-boards"}),
]
