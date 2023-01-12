from django.core.management.base import BaseCommand

from seeds.auth_user_seeder import AuthUserSeeder
from seeds.games_seeder import GamesSeeder
from seeds.group_seeder import GroupPermissionSeeder

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "Seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--refresh', action='store_true', default=False, help="Truncate table")

    def handle(self, *args, **options):
        refresh = False
        if options['refresh']:
            refresh = True

        # SEED DATA
        GroupPermissionSeeder().create(refresh)
        AuthUserSeeder().create(refresh)
        GamesSeeder().create(refresh)

        self.stdout.write("[DONE]\n")
