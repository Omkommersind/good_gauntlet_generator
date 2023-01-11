from django.utils.crypto import get_random_string

from backend.db.querysets import BaseCustomQuerySet
from users.enums import GroupsEnum


class UsersQuerySet(BaseCustomQuerySet):
    # Todo: inherit from standard user qs
    def normalize_email(self, email):
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email

    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        return get_random_string(length, allowed_chars)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})
