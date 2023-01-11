import os
import sys

from django.contrib.auth.models import Group

from users.enums import GroupsEnum
from users.models import UserModel


class AuthUserSeeder:

    def create(self, refresh=False):
        if refresh is True:
            self.truncate_table()

        self.create_superuser()
        self.create_moderator()

    @staticmethod
    def truncate_table():
        UserModel.objects.all().delete()
        sys.stdout.write("Truncate auth_user table ... [OK]\n")

    @staticmethod
    def create_superuser():
        if UserModel.objects.filter(username='admin').exists():
            sys.stdout.write('User admin already exists!\n')
            return False
        else:
            u = UserModel(
                is_superuser=True,
                username='admin',
                # email='superadmin@admin.com',
                is_staff=True,
                is_active=True,
            )
            u.set_password(os.getenv('SUPERUSER_PASS', 'admin'))
            u.save()

            sys.stdout.write("Superuser seed successful! [OK]\n")
            return u.id

    # Todo: refactor same cases
    @staticmethod
    def create_moderator(username='test_moderator', password=os.getenv('MODERATOR_PASS', 'moderator')):
        if UserModel.objects.filter(username=username).exists():
            sys.stdout.write('Moderator already exists!\n')
            return False
        else:
            u = UserModel(
                username=username,
                is_staff=True,
            )
            u.set_password(password)
            u.save()

            moderator_group = Group.objects.get(name=GroupsEnum.MODERATORS)
            u.groups.add(moderator_group)

            sys.stdout.write("Moderator seed successful! [OK]\n")
            return u.id
