from .user import User, readCSVDictUser
from .listing import InMemoryListing
from uuid import uuid4


class UserList(InMemoryListing):
    """utility class to read users from iterable"""

    _rows = None

    def __init__(self, list_csv_users):
        # Simply filter out any records which are False
        self._rows = list(
            filter(None, [_mapUsers(user) for user in list_csv_users]))

    def getColumns(self):
        """gets model columns that can be sortedon"""
        return ['pk', 'skills', 'name']

    def getUser(self, pk=1):
        return self.getEntry(pk)

    def addUser(self, newUser):
        self.addEntry(newUser)

    def addEntry(self, entry):
        if not type(entry) is User:
            raise ValueError("you can only add User instances to a UserList")

        self._rows.append(entry)

    def getEntry(self, pk=1):
        return list(filter(_pkMatch(pk), self._rows))[0]

    def getPagedResult(self, start, end, sortkey, sortorder):
        """return subset of records based on offset with order from list"""
        results = sorted(self._rows, key=_sortkey(sortkey), reverse=sortorder)
        return results[start:end]


def _pkMatch(value):
    def _matches(usr):
        return usr.getPK() == value

    return _matches


def _mapUsers(v):
    """utility class to read users from iterable"""
    # When given just dict value generate uuid pk
    if type(v) is dict:
        user = readCSVDictUser(v, str(uuid4()))
        return user
    # otherwise this is invalid / incompatible. add a case or filter
    return False


def _sortkey(key):
    # closure to support dynamic column binding
    def _sort(obj):
        if key == "name":
            return (obj.getName())
        elif key == "skills":
            return (len(obj.getSkills()))
        return (obj.getPK())

    return _sort
