import unittest

from .user import User, readCSVDictUser
from .errors import PermissionError

from datetime import datetime
import pytz


class UserTest(unittest.TestCase):
    def setUp(self):
        self.PrimaryUser = User(1, "Lewis", True, False, "GMT")

    def test_user_set_global_admin(self):
        result_table = [{
            "user": self.PrimaryUser,
            "initial": True,
            "change": True,
            "value": True
        }, {
            "user": User(3, "Brad", False, False, "UTC"),
            "initial": True,
            "change": False,
            "value": True
        }]
        for expectation in result_table:
            testUser = User(2, "Claire", expectation["initial"], False, "UTC")
            try:
                testUser.setGlobalAdmin(expectation["value"],
                                        expectation["user"])
            except PermissionError:
                pass
            if expectation["change"]:
                self.assertEqual(testUser.isGlobalAdmin(),
                                 expectation["value"])
            else:
                self.assertEqual(testUser.isGlobalAdmin(),
                                 expectation["initial"])

    def test_user_add_skill(self):
        result_table = [{
            "skills": ["c", "cpp", "java"],
            "expectedLength": 3
        }, {
            "skills": ["c", "cpp", "java", "c"],
            "expectedLength": 3
        }, {
            "skills": ["", "5", "java"],
            "expectedLength": 1
        }, {
            "skills": [
                "Clapping", "Cheese", "Cheering", "Tripe", "Hype", "Prancing",
                "Salsa", "Flamenco", "Cha-Cha-Cha", "Chancing", "Bob Johnson"
            ],
            "expectedLength":
            11
        }, {
            "skills": ["Clapping", "Hype", "Bob Johnson", "Hype"],
            "expectedLength": 3
        }]
        for expectation in result_table:
            testUser = User(1, "Lewis", True, False, "UTC")
            for skill in expectation["skills"]:
                try:
                    testUser.addSkill(skill)
                except Exception:
                    pass
            self.assertEqual(
                len(testUser.getSkills()), expectation["expectedLength"])

    def test_user_remove_skill(self):
        testUser = User(1, "Lewis", True, False, "UTC")
        for skill in [
                "Salsa", "Flamenco", "Cha-Cha-Cha", "Chancing", "Bob Johnson"
        ]:
            testUser.addSkill(skill)

        # check all skills have been added
        self.assertEqual(len(testUser.getSkills()), 5)

        # remove a known-skill and re-check
        testUser.removeSkill("Bob Johnson")
        self.assertEqual(len(testUser.getSkills()), 4)

        # try to remove known-non-skill, assert same
        testUser.removeSkill("Dick Cheney")
        self.assertEqual(len(testUser.getSkills()), 4)

    def test_user_set_external_id(self):
        result_table = [{
            "input": "i2502809511306",
            "result": "i2502809511306",
            "initial": None,
            "initialresult": None
        }, {
            "input": "",
            "result": None,
            "initial": "i2502809511306",
            "initialresult": "i2502809511306"
        }, {
            "input": None,
            "result": None,
            "initial": "i2502809511306",
            "initialresult": "i2502809511306"
        }, {
            "input": "invalid",
            "result": None,
            "initial": "",
            "initialresult": None
        }, {
            "input": "01234567891234",
            "result": "01234567891234",
            "initial": "invalid",
            "initialresult": None
        }]

        for expectation in result_table:
            testUser = User(7, "Sean Connery", True, False, "PST")
            try:
                testUser.setExternalId(expectation["initial"])
            except ValueError:
                pass
            self.assertEqual(
                expectation["initialresult"], testUser.getExternalId(),
                "Expected {}, Got {}".format(expectation["initialresult"],
                                             testUser.getExternalId()))

            try:
                testUser.setExternalId(expectation["input"])
            except ValueError:
                pass
            self.assertEqual(
                expectation["result"], testUser.getExternalId(),
                "Expected {}, Got {}".format(expectation["result"],
                                             testUser.getExternalId()))

    def test_can_change_timezone(self):
        result_table = [{
            "v": "PST",
            "exception": False
        }, {
            "v": "CST",
            "exception": False
        }, {
            "v": "EST",
            "exception": False
        }, {
            "v": "GMT",
            "exception": False
        }, {
            "v": "Bob the Builder",
            "exception": True
        }, {
            "v": "Mars",
            "exception": True
        }]

        for expectation in result_table:
            testUser = User(1, "Lewis", True, False, "UTC")
            if expectation["exception"]:
                with self.assertRaises(ValueError):
                    testUser.changeTimeZone(expectation["v"])
                self.assertNotEqual(testUser.getTimeZone(), expectation["v"])
            else:
                testUser.changeTimeZone(expectation["v"])
                self.assertEqual(testUser.getTimeZone(), expectation["v"])

    def test_can_change_marketing_preferences(self):
        preferences = self.PrimaryUser.getMarketingPreferences()
        self.assertEqual(preferences, False, "Expected {}, Got {}".format(
            False, preferences))
        self.PrimaryUser.changeMarketingPreferences(True)
        preferences = self.PrimaryUser.getMarketingPreferences()
        self.assertEqual(preferences, True, "Expected {}, Got {}".format(
            True, preferences))

    def test_can_turn_user_into_dict(self):
        self.PrimaryUser.addSkill("API")
        dictUser = self.PrimaryUser.toDict()
        self.assertDictEqual(
            dictUser, {
                "pk": 1,
                "name": "Lewis",
                "email": None,
                "global_admin": True,
                "timezone": "GMT",
                "receive_marketing": False,
                "external_id": None,
                "skills": ["API"]
            })

    def test_parsing_csv_dict_not_dict_returns_false(self):
        result = readCSVDictUser(42, 1)
        self.assertFalse(result)

    def test_parsing_csv_dict_invalid_dict_returns_false(self):
        result = readCSVDictUser({"mynameis": "not user dictionary"}, 1)
        self.assertFalse(result)

    def test_parsing_valid_csv_dict_returns_user_class(self):
        users = [{
            "email": "scott.baker@ux.io",
            "name": "Scott Baker",
            "global_admin": "f",
            "_timezone": "PST",
            "receive_marketing": "f",
            "external_id": "s7754756893610",
            "Skills": "Dancing, Prancing"
        }, {
            "email": None,
            "name": "Jet Li",
            "global_admin": "T",
            "_timezone": "GMT",
            "receive_marketing": "f",
            "external_id": "",
            "Skills": "Being the one, High-kicks"
        }, {
            "email": "hi",
            "name": "Scott Baker",
            "global_admin": "malformed entry",
            "_timezone": "invalid",
            "receive_marketing": "T",
            "external_id": "invalid",
            "Skills": "22"
        }]
        for usr in users:
            result = readCSVDictUser(usr, 1)
            self.assertIsInstance(result, User)

    def test_user_change_name_empty_string(self):
        with self.assertRaises(ValueError):
            self.PrimaryUser.changeName("")

    def test_user_change_name_invalid(self):
        with self.assertRaises(ValueError):
            self.PrimaryUser.changeName("1")

    def test_user_change_name_none(self):
        with self.assertRaises(ValueError):
            self.PrimaryUser.changeName(None)

    def test_user_change_name_valid_single(self):
        originalName = self.PrimaryUser.getName()
        self.PrimaryUser.changeName("Zed")
        self.assertNotEqual(originalName, self.PrimaryUser.getName())

    def test_user_change_name_valid_multi(self):
        originalName = self.PrimaryUser.getName()
        self.PrimaryUser.changeName("Horacio Archibald 3rd")
        self.assertNotEqual(originalName, self.PrimaryUser.getName())

    def test_user_set_email_none(self):
        originalEmail = self.PrimaryUser.getEmail()
        self.PrimaryUser.changeEmail(None)
        self.assertNotEqual(originalEmail, self.PrimaryUser.getEmail)

    def test_user_set_email_empty_string(self):
        originalEmail = self.PrimaryUser.getEmail()
        self.PrimaryUser.changeEmail("")
        self.assertNotEqual(originalEmail, self.PrimaryUser.getEmail)

    def test_user_set_email_shortest(self):
        originalEmail = self.PrimaryUser.getEmail()
        self.PrimaryUser.changeEmail("a@b.c")
        self.assertNotEqual(originalEmail, self.PrimaryUser.getEmail)

    def test_user_set_email_invalid(self):
        with self.assertRaises(ValueError):
            self.PrimaryUser.changeEmail("you-wot-m8")

    def test_user_get_time(self):
        dt = datetime(1999, 1, 22, 12, 0, 0, tzinfo=pytz.utc)
        output = self.PrimaryUser.getTime(dt)
        self.assertTrue(output, "12:00:00 GMT")
