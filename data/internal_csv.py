from backports import csv

import io


class CSVReader(object):
    """Abstract Interface for Consuming Marshalled CSV"""
    _headers = []

    _rows = []

    def getHeaders(self):
        """Get a list of headers"""
        return self._headers

    def getRow(self, row=1):
        """Get a specific row of key->value strings"""
        return self._rows[row]

    def getAll(self):
        """Get all rows"""
        return self._rows[:]

    def _parseCSV(self, file):
        """read CSV from IO using DictReader"""
        i = 1
        reader = csv.DictReader(file)
        self._headers = list(reader.fieldnames)
        for row in reader:
            self._rows.append(row.copy())
            i += 1


class CSVFileReader(CSVReader):
    """read CSV from file by filename"""

    def __init__(self, filename):
        self._headers = []
        self._rows = []

        with io.open(filename, encoding='utf-8') as file:
            self._parseCSV(file)


class CSVStringReader(CSVReader):
    """read CSV from string (unicode)"""

    def __init__(self, csvstring):
        self._headers = []
        self._rows = []

        file = io.StringIO(csvstring)
        self._parseCSV(file)
