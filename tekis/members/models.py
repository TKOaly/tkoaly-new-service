from __future__ import unicode_literals
import hashlib

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.crypto import salted_hmac
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


ROLE_CHOICES = (
    (None, _("Nothing")),
    ("jasenvirkailija", _("Member officer")),
    ("kayttaja", _("Member")),
    ("virkailija", _("Officer")),
    ("yllapitaja", _("Administrator")),
    ("tenttiarkistovirkailija", _("Exam archive officer"))
)

MEMBERSHIP_CHOICES = (
    (None, _("Nothing")),
    ("ei-jasen", _("Non-member")),
    ("erotettu", _("Membership revoked")),
    ("ulkojasen", _("External member")),
    ("jasen", _("Member")),
    ("kannatusjasen", _("Sponsor member")),
    ("kunniajasen", _("Honor member"))
)


class TekisMember(models.Model):
    """Remote member model used for authentication"""
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    email = models.EmailField()
    residence = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    hyy_member = models.BooleanField()
    membership = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    role = models.CharField(max_length=40, choices=ROLE_CHOICES)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    hashed_password = models.CharField(max_length=40)
    salt = models.CharField(max_length=20)
    tktl = models.BooleanField()
    deleted = models.BooleanField()

    def __unicode__(self):
        return self.username

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct.
        """
        czech = hashlib.sha1((
            self.salt
            + getattr(settings, "SITE_LOGIN_SALT", "heiinmpi")
            + raw_password).encode('utf-8')).hexdigest()
        return czech == self.hashed_password

    def save(self, *args, **kwargs):
        raise NotImplementedError("Read-only model!")

    class Meta:
        managed = False
        db_table = "users"


def add_member(role):
    from django.utils.timezone import now
    # testing user creation
    return TekisMember.objects.create(
        username=role,
        name=role,
        screen_name=role,
        email="%s@%s.fi" % (role, role),
        residence="kerava",
        phone=role,
        hyy_member=True,
        membership="jasen",
        role=role,
        created=now(),
        modified=now(),
        hashed_password='bf97b090e2ec03c39dd5e6cde5b48c3fc4b1bc87',
        salt="abc",
        tktl=True,
        deleted=False
    )
