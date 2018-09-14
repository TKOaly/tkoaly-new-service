from __future__ import unicode_literals

from django.contrib.auth.models import Group, User

from tekis.members.models import TekisMember


class TekisAuthBackend(object):
    """Backend that authenticates with the members database and creates a
    full Django user object if it succeeds

    """

    def authenticate(self, username=None, password=None):
        try:
            member = TekisMember.objects.get(username=username)
        except TekisMember.DoesNotExist:
            return None
        if not member.check_password(password):
            return None
        # create or update a Django user
        name = member.screen_name.split()
        fn = name[0]
        ln = name[-1]

        user, created = User.objects.get_or_create(
            username=member.username,
            defaults={
                "username": member.username,
                "email": member.email,
                "first_name": fn,
                "last_name": ln,
                "date_joined": member.created,
            }
        )

        # always update permissions
        user.is_staff = member.role in ["virkailija",
                                        "jasenvirkailija",
                                        "yllapitaja"]
        user.is_superuser = member.role == "yllapitaja"
        user.is_active = member.membership not in ["ei-jasen", "erotettu"]
        user.save()

        # add and remove non-superuser permission group relationships
        # "yllapitaja" is a superuser so he doesn't need any groups
        virkailija, _ = Group.objects.get_or_create(name="virkailija")
        if member.role == "virkailija":
            user.groups.add(virkailija)
        else:
            user.groups.remove(virkailija)

        jasenvirkailija, _ = Group.objects.get_or_create(name="jasenvirkailija")
        if member.role == "jasenvirkailija":
            user.groups.add(jasenvirkailija)
        else:
            user.groups.remove(jasenvirkailija)

        # bail out inactive users here
        if not user.is_active:
            return None

        return user


    def get_user(self, user_id):
       try:
           return User.objects.get(pk=user_id)
       except User.DoesNotExist:
           return None
