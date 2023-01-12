import sys

from games.models import GameModel, PlatformModel
from seeds.utils import seed_objects_from_csv


class GamesSeeder:
    def create(self, refresh=False):
        if refresh is True:
            self.truncate_table()

        seed_objects_from_csv('static/platforms.csv', PlatformModel)
        seed_objects_from_csv('static/games.csv', GameModel)

    # TRUNCATE TABLE
    def truncate_table(self):
        GameModel.default_manager.all().delete()
        sys.stdout.write("Truncate games table ... [OK]\n")

