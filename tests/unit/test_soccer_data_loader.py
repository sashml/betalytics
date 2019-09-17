import unittest

from betalytics.soccer.loader.football_data_loader import load_and_normalize_data
from betalytics.common.test_utils import ordered


class TestSoccerDataLoader(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSoccerDataLoader, self).__init__(*args, **kwargs)
        self.db = None

    @ordered
    def test_initial_load(self):
        """
        Test the Loader loads data properly
        """
        self.db = load_and_normalize_data(db_file_name=r'../../data/database.sqlite', bookie='BET365')
        self.assertEqual(self.db.shape[1], 13)

    @ordered
    def test_todo(self):
        """

        """
        pass


if __name__ == '__main__':
    unittest.main()
