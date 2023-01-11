import sys

from django.contrib.auth.models import Group, Permission

from users.enums import GroupsEnum


class GroupPermissionSeeder:
    def create(self, refresh=False):
        if refresh is True:
            self.truncate_table()

        self.create_all_groups_with_permissions()

    # TRUNCATE TABLE
    def truncate_table(self):
        Group.objects.all().delete()
        sys.stdout.write("Truncate group table ... [OK]\n")

    def create_all_groups_with_permissions(self):
        moderators = Group.objects.get_or_create(name=GroupsEnum.MODERATORS)[0]
        moderators.permissions.clear()
        moderators_permissions_codenames = [
            'view_usermodel',
            'create_usermodel',
            'delete_usermodel',
        ]
        moderators_permissions = Permission.objects.filter(codename__in=moderators_permissions_codenames)
        moderators.permissions.add(*moderators_permissions)
