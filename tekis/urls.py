"""tekis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.utils import translation
from django.utils.translation import ugettext as _
from django.contrib.auth.views import login, logout
from django.shortcuts import render

from tekis.flatpages.views import flatpage
from tekis.members.api import MemberDetailsView

def index(request):
    return render(request, "index.html")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^oauth/', include('tekis.oauth', namespace='oauth2_provider')),
    url(r'^api/v1/', include([
        url('^me/$', MemberDetailsView.as_view(), name="api-member"),
    ])),
    url(r'^$', index, name="index"),
]

# eagerly populate all localized urls to avoid awkward 404s on deeplinks
cur_language = translation.get_language()
try:
    for lang_code, language in settings.LANGUAGES:
        translation.activate(lang_code)
        urlpatterns.extend([
            url(_(r'^board/'), include('tekis.board.urls')),
            url(_(r'^login/$'), login, name="login", ),
            url(_(r'^logout/$'), logout, name="logout"),
        ])
finally:
    translation.activate(cur_language)

urlpatterns.extend(
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

urlpatterns.extend([
    url(r'^(?P<url>.*)$', flatpage, name='flatpage'),
])
