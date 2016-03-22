"glue code to make oauth work right"

from django import forms
from django.conf.urls import url, include
from django.views.generic import TemplateView

from oauth2_provider import views as oauth_views
from oauth2_provider.models import Application

class UserApplicationUpdateForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "redirect_uris"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "redirect_uris": forms.Textarea(attrs={"class": "form-control"}),
        }

class UserApplicationRegisterForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["name", "redirect_uris",
                  "client_type", "authorization_grant_type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "redirect_uris": forms.Textarea(attrs={"class": "form-control"}),
            "client_type": forms.Select(attrs={"class": "form-control"}),
            "authorization_grant_type": forms.Select(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        kwargs["initial"] = {"client_type": "confidential",
                             "authorization_grant_type": "authorization-code"}
        super(UserApplicationRegisterForm, self).__init__(*args, **kwargs)

class UserApplicationUpdate(oauth_views.ApplicationUpdate):
    form_class = UserApplicationUpdateForm
    fields = None

class UserApplicationRegistration(oauth_views.ApplicationRegistration):
    def get_form_class(self): return UserApplicationRegisterForm

class IndexView(TemplateView):
    template_name = "oauth2_provider/index.html"

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^authorize/$', oauth_views.AuthorizationView.as_view(),
        name="authorize"),
    url(r'^token/$', oauth_views.TokenView.as_view(),
        name="token"),
    url(r'^revoke_token/$', oauth_views.RevokeTokenView.as_view(),
        name="revoke-token"),
    # ---
    url(r'^applications/', include([
        url(r'^$', oauth_views.ApplicationList.as_view(), name="list"),
        url(r'^register/$', UserApplicationRegistration.as_view(),
            name="register"),
        url(r'^(?P<pk>\d+)/$', oauth_views.ApplicationDetail.as_view(),
            name="detail"),
        url(r'^(?P<pk>\d+)/delete/$', oauth_views.ApplicationDelete.as_view(),
                name="delete"),
        url(r'^(?P<pk>\d+)/update/$', UserApplicationUpdate.as_view(),
                name="update"),
    ])),
    url(r'^authorized_tokens/', include([
        url(r'^$', oauth_views.AuthorizedTokensListView.as_view(),
            name="authorized-token-list"),
        url(r'^(?P<pk>\d+)/delete/$', oauth_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]))
]
