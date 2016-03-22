from django.http import JsonResponse

from oauth2_provider.views.generic import ProtectedResourceView


class MemberDetailsView(ProtectedResourceView):
    def get(self, request):
        u = request.resource_owner
        role = "jasen"
        if u.is_staff:
            role = "virkailija"
        if u.is_superuser:
            role = "yllapitaja"

        return JsonResponse({
            "content": {
                "username": u.username,
                "real_name": u.get_full_name(),
                "role": role
            }
        })
