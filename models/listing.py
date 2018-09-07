class AbstractListing(object):
    def getListing(self, limit, page):
        """return a tuple of listing data and support information"""
        raise RuntimeError("Implement please")

    def getTotal(self):
        """return the total number of records in a listing"""
        raise RuntimeError("this is an abstract listing")

    def getLimit(self, limit):
        """return bounded numeric limit between 1 & 100. 10 if invalid"""
        # set default limit
        if limit is None:
            limit = 10
        # bound to between 1 and 100
        return min(max(int(limit), 1), 100)

    def getPages(self, limit, total):
        """return number of pages given page record limit and total records"""

        if not type(limit) is int or not type(total) is int:
            return 1

        if limit < 1 or total < 1:
            return 1

        pages = int(total / limit)
        if bool((total % limit) != 0):
            pages += 1  # special case for remainder
        return pages

    def getPage(self, page, pages):
        """return number of page. bounds between 1 and number of pages."""
        if page is None:
            return 1
        # bound to between 1 and pages
        return max(1, min(page, pages))

    def getStart(self, page, limit):
        """return offset based on page and limit"""
        return ((page - 1) * limit)

    def getEnd(self, start, limit, total):
        """return offset based on page and limit and starting position"""
        return start + min(limit, (total - start))

    def getPagedResult(self, start, end, sortkey, sortorder):
        """return subset of records based on offset with order"""
        raise RuntimeError("this is an abstract listing")

    def getEntry(self, pk=1):
        """return specific record based on primary-key"""
        raise RuntimeError("this is an abstract listing")

    def addEntry(self, entry):
        """add specific record"""
        raise RuntimeError("this is an abstract listing")


class InMemoryListing(AbstractListing):
    _rows = []

    def getColumns(self):
        """gets model columns that can be sortedon"""
        return ['pk']

    def getSortingInfo(self, sortfield, sortdesc):
        """retrieves sortinginfo from input"""
        columns = self.getColumns()
        column = columns[0] if sortfield not in columns else sortfield
        sortdesc = bool(sortdesc == 'DESC')
        return (column, sortdesc)

    def getListing(self, _limit, _page, sortfield, sortdesc):
        """get listing data"""
        total = self.getTotal()
        limit = self.getLimit(_limit)
        pages = self.getPages(limit, total)
        page = self.getPage(_page, pages)
        start = self.getStart(page, limit)
        end = self.getEnd(start, limit, total)

        # sort the results
        column, sortdesc = self.getSortingInfo(sortfield, sortdesc)

        results = self.getPagedResult(start, end, column, sortdesc)
        count = len(results)
        return (results, page, pages, limit, count, column, sortdesc, total)

    def __init__(self):
        self._rows = []

    def getTotal(self):
        """return the total number of records in a listing from list"""
        return len(self._rows)

    def getPagedResult(self, start, end, sortkey, sortorder):
        """return subset of records based on offset with order from list"""
        results = sorted(self._rows, key=_sortkey(sortkey), reverse=sortorder)
        return results[start:end]

    def getEntry(self, pk=1):
        """return specific record based on primary-key from list"""
        return self._rows[pk]

    def addEntry(self, entry):
        """add specific record to list"""
        self._rows.append(entry)
        return len(self._rows) - 1


def _sortkey(key):
    # closure to support dynamic column binding
    def _sort(obj):
        if type(obj) is dict:
            if type(obj[key]) in [str]:
                return (str(obj[key]).lower())
            elif type(obj[key]) in [slice, list]:
                return (len(obj[key]))
            return (obj[key])
        return obj

    return _sort
