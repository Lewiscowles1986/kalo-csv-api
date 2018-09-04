import unittest

from .internal_csv import CSVStringReader, CSVFileReader


class ParseCSVTest(unittest.TestCase):
    def setUp(self):
        self.Reader = CSVFileReader('users.csv')

    def test_csv_expected_headers(self):
        self.assertEqual(self.Reader.getHeaders(), [
            'email', 'name', 'global_admin', '_timezone', 'receive_marketing',
            'external_id', 'Skills'
        ])

    def test_csv_read_data_team_name(self):
        self.assertEqual(self.Reader.getRow(row=0).get('name'), 'Scott Baker')

    def test_csv_read_data_points(self):
        self.assertEqual(
            self.Reader.getRow(row=20).get('external_id'), 's6249101375190')

    def test_csv_get_all(self):
        reader = CSVStringReader(u"""name,age,skills
\"Michael Jordan\",45,\"Slam Dunking, Ball Spinning, 90's\"""")
        empty = reader.getAll()
        self.assertEqual(len(empty), 1)
