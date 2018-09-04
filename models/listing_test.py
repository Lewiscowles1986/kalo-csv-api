import unittest
from random import randint
from builtins import IndexError

from .listing import InMemoryListing


class ListingTest(unittest.TestCase):
    def test_get_start_10_100_900(self):
        myList = InMemoryListing()
        start = myList.getStart(10, 100)
        self.assertEqual(start, 900)

    def test_get_end_1000_10_2000_1010(self):
        myList = InMemoryListing()
        end = myList.getEnd(1000, 10, 2000)
        self.assertEqual(end, 1010)

    def test_get_end_1000_10_1003_1003(self):
        myList = InMemoryListing()
        end = myList.getEnd(1000, 10, 1003)
        self.assertEqual(end, 1003)

    def test_get_page_10_100_10(self):
        myList = InMemoryListing()
        page = myList.getPage(10, 100)
        self.assertEqual(page, 10)

    def test_get_page_52_7_7(self):
        myList = InMemoryListing()
        page = myList.getPage(52, 7)
        self.assertEqual(page, 7)

    def test_get_page_1_0_1(self):
        myList = InMemoryListing()
        page = myList.getPage(1, 0)
        self.assertEqual(page, 1)

    def test_get_page_none_50_1(self):
        myList = InMemoryListing()
        page = myList.getPage(None, 50)
        self.assertEqual(page, 1)

    def test_get_pages_10_100_10(self):
        myList = InMemoryListing()
        pages = myList.getPages(10, 100)
        self.assertEqual(pages, 10)

    def test_get_pages_7_52_8(self):
        myList = InMemoryListing()
        pages = myList.getPages(7, 52)
        self.assertEqual(pages, 8)

    def test_get_pages_0_0_1(self):
        myList = InMemoryListing()
        pages = myList.getPages(0, 0)
        self.assertEqual(pages, 1)

    def test_get_limit_with_none_between_1_and_100(self):
        myList = InMemoryListing()
        limit = myList.getLimit(None)
        self.assertGreaterEqual(limit, 1)
        self.assertLessEqual(limit, 100)

    def test_get_limit_always_between_1_and_100(self):
        for i in range(0, 100):
            myList = InMemoryListing()
            limit = myList.getLimit(randint(-999, 999))
            self.assertGreaterEqual(limit, 1)
            self.assertLessEqual(limit, 100)

    def test_get_limit_100_between_1_and_100(self):
        for i in range(0, 100):
            myList = InMemoryListing()
            limit = myList.getLimit(100)
            self.assertGreaterEqual(limit, 1)
            self.assertLessEqual(limit, 100)

    def test_in_memory_empty(self):
        myList = InMemoryListing()
        self.assertEqual(myList.getTotal(), 0)
        result = myList.getPagedResult(0, 99, 'id', False)
        self.assertEqual(len(result), 0)
        with self.assertRaises(IndexError):
            myList.getEntry(pk=1)

    def test_in_memory_n(self):
        for i in [1, 2, 3, 100]:
            myList = InMemoryListing()
            # Create n entries
            for j in range(0, i):
                myList.addEntry("string")

            self.assertEqual(myList.getTotal(), i)
            result = myList.getPagedResult(0, 100, 'id', False)
            self.assertEqual(len(result), i)
            # using -1 to get last item.
            for j in range(0, i):
                self.assertEqual(type(myList.getEntry(pk=j)), str)

    def test_in_memory_simple_penny_invoice_sort(self):
        myList = InMemoryListing()
        # Create n entries
        maxPrice = 0
        total = 0
        for i in range(0, 5):
            price = randint(1, 10000) + 0
            myList.addEntry({"item": "thing", "price": price})
            maxPrice = max(maxPrice, price)
            total += price

        self.assertEqual(myList.getTotal(), 5)
        result = myList.getPagedResult(0, 100, 'price', True)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["price"], maxPrice)
        self.assertEqual(sum(list(map(lambda x: (x["price"]), result))), total)

    def test_in_memory_multiple_penny_invoice_sort(self):
        myList = InMemoryListing()
        # Create n entries
        maxTotal = 0
        maxItems = 0
        for i in range(0, 5):
            total = 0
            myList.addEntry({"reference": "REF-%06d" % i, "items": []})
            invoice = myList.getEntry(pk=-1)
            for j in range(0, randint(1, 10)):
                price = randint(1, 10000) + 0
                invoice["items"].append({"item": "thing", "price": price})
                total += price
            maxItems = max(maxItems, len(invoice["items"]))
            invoice["total"] = total
            maxTotal = max(maxTotal, total)

        result = myList.getPagedResult(0, 100, 'items', True)
        # print("Listing:")
        # print(dumps(result))
        self.assertEqual(len(result), 5)
        self.assertEqual(len(result[0]["items"]), maxItems)

        result = myList.getPagedResult(0, 100, 'total', True)
        # print("Total:")
        # print(dumps(result))
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["total"], maxTotal)

        result = myList.getPagedResult(0, 100, "reference", True)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["reference"], "REF-000004")

        result = myList.getPagedResult(0, 100, "reference", False)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0]["reference"], "REF-000000")
