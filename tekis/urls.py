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
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.views import login, logout
from django.shortcuts import render

from tekis.flatpages.views import flatpage

def index(request):
    return render(request, "index.html")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(_(r'^board/'), include('tekis.board.urls')),
    url(_(r'^login/$'), login, name="login", ),
    url(_(r'^logout/$'), logout, name="logout"),
    url(r'^$', index, name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^(?P<url>.*)$', flatpage, name='flatpage'),
]
