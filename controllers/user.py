from datetime import datetime

from flask import Blueprint, jsonify, request, Response
from uuid import uuid4
from flask_json_multidict import get_json_multidict

from hateoas.listing import genPagingInfo, genLinks
from hateoas.link import link
from models.user import User
from models.userlist import UserList
from data.internal_csv import CSVFileReader
from forms.user import UserForm
from data.user import userHateoasLinks

user = Blueprint('user', __name__)

reader = CSVFileReader('users.csv')
users = UserList(reader.getAll())

def get_data(request):
    return get_json_multidict(request) if request.is_json else request.form

@user.route('/', methods=['GET'], strict_slashes = False)
def index():
    results, page, pages, limit, count, column, desc, total = users.getListing(
        request.args.get('limit'), request.args.get('page'), 
        request.args.get('sortby'), request.args.get('order'))

    return jsonify({
        "data": addUserLinks(results),
        "links": genLinks("/users/", page, pages, limit),
        "paging": genPagingInfo(total, limit, pages, count, page),
        "sort": {
            "sortby": column,
            "sortdesc": desc
        }
    })


@user.route('/<string:pk>/time', methods=['GET'])
def time(pk):
    try:
        user = users.getUser(pk=pk)
        return jsonify({
            "data": {
                "name": user.getName(),
                "time": user.getTime(datetime.utcnow())
            },
            "links": [link("/users/", "listing", "GET")]
        }), 200
    except IndexError:
        return Response("User not found", 404)


@user.route('/', methods=['POST'], strict_slashes = False)
def create():
    form = UserForm(get_data(request))

    if form.validate():
        newUser = User(
            str(uuid4()), form.name.data, False, form.receive_marketing.data,
            form.timezone.data)
        skills = list(filter(None, form.skills.data.split(',')))
        [newUser.addSkill(skill.strip()) for skill in skills]
        newUser.setExternalId(form.external_id.data)
        newUser.changeEmail(form.email.data)
        users.addUser(newUser)
        return jsonify({
            "data":
            newUser.toDict(),
            "links": userHateoasLinks(newUser)
        }), 201

    return jsonify({"errors": list(form.errors.items())}), 400


@user.route('/<string:pk>', methods=['PUT'], strict_slashes = False)
def update(pk):
    try:
        user = users.getUser(pk=pk)
        form = UserForm(get_data(request))
        if form.validate():
            user.changeName(form.name.data)
            user.changeMarketingPreferences(form.receive_marketing.data)
            user.changeTimeZone(form.timezone.data)
            skills = list(filter(None, form.skills.data.split(',')))
            [user.addSkill(skill.strip()) for skill in skills]
            user.setExternalId(form.external_id.data)
            user.changeEmail(form.email.data)
            return jsonify({
                "data":
                user.toDict(),
                "links": userHateoasLinks(user)
            }), 200
        return jsonify({"errors": list(form.errors.items())}), 400
    except IndexError:
        return Response("User not found", 404)


def addUserLinks(results):
    out = []
    for result in results:
        out.append({"data": result.toDict()})
        out[-1]["links"] = [
            link("/users/%s/time" % result.getPK(), "time", "GET")
        ]
    return out
