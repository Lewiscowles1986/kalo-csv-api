from tzhelper import get_timezones, get_time
import re
import six

from .errors import PermissionError


class User(object):
    """storage-tier agnostic model for user logic"""
    _pk = 0
    _name = ""
    _global_admin = False
    _receive_marketing = False
    _timezone = "UTC"
    _skills = None
    _external_id = None

    def __init__(self, pk, name, global_admin, receive_marketing, timezone):
        """constructor for user model containing required fields"""
        self._pk = pk
        self._name = name
        self._global_admin = global_admin
        self._receive_marketing = receive_marketing
        self._timezone = timezone
        self._skills = set()
        self._external_id = None
        self._email = None

    def getPK(self):
        return str(self._pk)

    def addSkill(self, skill):
        """adds a skill to user set of skills"""
        if len(skill) < 1:
            raise ValueError("Skill name has to have length > 0")

        # See: https://regex101.com/r/ropSNz/1/ for tests run
        if re.match(r"^[a-zA-Z]+[a-zA-Z0-9 -]*$", skill) is None:
            raise ValueError("Skill name has to start with a letter and " +
                             "can only contain letters numbers & spaces")

        self._skills.add(str(skill).rstrip())

    def removeSkill(self, skill):
        """removes a skill to user set of skills"""
        try:
            self._skills.remove(skill)
        except KeyError:
            pass

    def getSkills(self):
        """gets list of user skills"""
        return list(self._skills)

    def getExternalId(self):
        """retrieves the external_id of a user"""
        return self._external_id

    def setExternalId(self, external_id):
        """attempt to set the external_id of a user. else raise ValueError"""
        if external_id is None:
            external_id = ""
        fkLength = len(str(external_id))
        if fkLength > 0:
            # Examining CSV in Excel looks like external ID's are all 14 chars
            if fkLength != 14:
                raise ValueError("If set, external ID Must be 14 characters, "
                                 + "got: {}".format(fkLength))
            self._external_id = external_id
        else:
            self._external_id = None

    def getEmail(self):
        """retrieve user email"""
        return self._email

    def changeEmail(self, email):
        """attempt to set valid email of a user. else raise ValueError"""
        if email is None:
            email = ""
        emailLength = len(str(email))

        # early exit
        if emailLength == 0:
            self._email = None
            return

        atIndex = 0
        try:
            atIndex = str(email).index("@", 1)
        except ValueError:
            pass

        # min email a@b.c
        if emailLength > 3 and atIndex < emailLength - 2 and atIndex > 0:
            self._email = email
        else:
            raise ValueError("Invalid email supplied")

    def changeMarketingPreferences(self, allowed):
        """set user marketing preferences"""
        self._receive_marketing = bool(allowed)

    def getMarketingPreferences(self):
        """get user marketing preferences"""
        return self._receive_marketing

    def setGlobalAdmin(self, isGlobalAdmin, user):
        """set user as global admin as user. requires user to be GA"""
        if not user.isGlobalAdmin():
            raise PermissionError("Only global admin users can do that")
        self._global_admin = bool(isGlobalAdmin)

    def isGlobalAdmin(self):
        """check if user is global admin"""
        return bool(self._global_admin)

    def getName(self):
        """get user name"""
        return self._name + ""

    def changeName(self, newName):
        """change user name. raises ValueError if empty name provided"""
        if not isinstance(newName, six.string_types):
            newName = ""
        if len(newName) < 1:
            raise ValueError('Name Must be at least 1 characters')
        if newName[0].isdigit():
            raise ValueError('Names cannot start with numbers')
        self._name = newName

    def changeTimeZone(self, newTZ):
        """sets user timezone. raises ValueError if invalid timezone"""
        if newTZ in get_timezones():
            self._timezone = newTZ
        else:
            raise ValueError('Invalid TimeZone ' + newTZ)

    def getTimeZone(self):
        """gets user timezone"""
        return self._timezone

    def getTime(self, now):
        """gets the user-local time for a user at a given datetime"""
        user_tz = self.getTimeZone()
        time = get_time(user_tz, now)
        return "{} {}".format(time.strftime('%H:%M:%S'), user_tz)

    def toDict(self):
        """output dictionary representing public fields"""
        return {
            "pk": self._pk,
            "name": self._name,
            "email": self._email,
            "global_admin": self._global_admin,
            "timezone": self._timezone,
            "receive_marketing": self._receive_marketing,
            "external_id": self._external_id,
            "skills": list(self._skills)
        }


def readCSVDictUser(item, pk):
    """utility method to transform CSV expected data + row to user object"""
    if not isinstance(item, dict):
        return False

    if ("name" not in item or "global_admin" not in item
            or "receive_marketing" not in item or "_timezone" not in item
            or "email" not in item or "external_id" not in item):
        return False

    global_admin = item["global_admin"] is "T"
    receive_marketing = item["receive_marketing"] is "T"

    skills = []

    if isinstance(item["Skills"], six.string_types):
        skills = item["Skills"].split(",")

    return parseUserData(pk, item["name"], global_admin, receive_marketing,
                         item["email"], item["external_id"], item["_timezone"],
                         skills)


def parseUserData(pk, name, global_admin, receive_marketing, email,
                  external_id, timezone, skills):
    """utility method use to create user from values bypass exceptions"""
    # Create all users with UTC timezone. It will always be a valid timezone
    user = User(pk, name, global_admin, receive_marketing, 'UTC')

    for skill in skills:
        try:
            user.addSkill(skill.strip())
        except ValueError:
            pass

    try:
        user.changeEmail(email)
    except ValueError:
        pass

    try:
        user.changeTimeZone(timezone)
    except ValueError:
        pass

    try:
        user.setExternalId(external_id)
    except ValueError:
        pass

    return user
