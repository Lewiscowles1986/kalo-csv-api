import unittest

from hateoas.listing import genPagingInfo, genLinks, linkUri, link


class TestHATEOASHelpers(unittest.TestCase):
    def test_first_page_single_page_3_listing_links(self):
        links = genLinks("/somewhere", 1, 1, 10)
        expected = [
            link(linkUri("/somewhere", 1, 10), "first", "GET"),
            link(linkUri("/somewhere", 1, 10), "current", "GET"),
            link(linkUri("/somewhere", 1, 10), "last", "GET")
        ]

        self.assertEqual(len(links), len(expected))
        self.assertEqual(len(expected), 3)
        for curLink in links:
            idx = links.index(curLink)
            self.assertDictEqual(links[idx], expected[idx])

    def test_first_page_two_pages_4_listing_links(self):
        links = genLinks("/somewhere", 1, 2, 10)
        expected = [
            link(linkUri("/somewhere", 1, 10), "first", "GET"),
            link(linkUri("/somewhere", 1, 10), "current", "GET"),
            link(linkUri("/somewhere", 2, 10), "next", "GET"),
            link(linkUri("/somewhere", 2, 10), "last", "GET")
        ]

        self.assertEqual(len(links), len(expected))
        self.assertEqual(len(expected), 4)
        for curLink in links:
            idx = links.index(curLink)
            self.assertDictEqual(links[idx], expected[idx])

    def test_second_page_two_pages_4_listing_links(self):
        links = genLinks("/somewhere", 2, 2, 10)
        expected = [
            link(linkUri("/somewhere", 1, 10), "first", "GET"),
            link(linkUri("/somewhere", 1, 10), "prev", "GET"),
            link(linkUri("/somewhere", 2, 10), "current", "GET"),
            link(linkUri("/somewhere", 2, 10), "last", "GET")
        ]

        self.assertEqual(len(links), len(expected))
        self.assertEqual(len(expected), 4)
        for curLink in links:
            idx = links.index(curLink)
            self.assertDictEqual(links[idx], expected[idx])

    def test_second_page_three_pages_5_listing_links(self):
        links = genLinks("/somewhere", 2, 3, 10)
        expected = [
            link(linkUri("/somewhere", 1, 10), "first", "GET"),
            link(linkUri("/somewhere", 1, 10), "prev", "GET"),
            link(linkUri("/somewhere", 2, 10), "current", "GET"),
            link(linkUri("/somewhere", 3, 10), "next", "GET"),
            link(linkUri("/somewhere", 3, 10), "last", "GET")
        ]

        self.assertEqual(len(links), len(expected))
        self.assertEqual(len(expected), 5)
        for curLink in links:
            idx = links.index(curLink)
            self.assertDictEqual(links[idx], expected[idx])

    def test_gen_paging_info(self):
        self.assertDictEqual(
            genPagingInfo(97, 10, 10, 7, 10), {
                "total": 97,
                "limit": 10,
                "pages": 10,
                "count": 7,
                "page": 10
            })
