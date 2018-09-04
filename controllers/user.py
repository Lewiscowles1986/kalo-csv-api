from datetime import datetime

from flask import Blueprint, jsonify, request, Response
from uuid import uuid4

from hateoas.listing import genPagingInfo, genLinks
from hateoas.link import link
from models.user import User
from models.userlist import UserList
from data.internal_csv import CSVFileReader
from forms.user import UserForm

user = Blueprint('user', __name__)

reader = CSVFileReader('users.csv')
users = UserList(reader.getAll())


@user.route('/', methods=['GET'])
def index():
    total = users.getTotal()
    limit = users.getLimit(request.args.get('limit'))
    pages = users.getPages(limit, total)
    page = users.getPage(request.args.get('page'), pages)
    start = users.getStart(page, limit)
    end = users.getEnd(start, limit, total)

    # sort the results
    columns = ['pk', 'name', 'skills']
    column = request.args.get('sortby')
    if column not in columns:
        column = columns[0]
    sortdesc = bool(request.args.get('order') == 'DESC')

    results = users.getPagedResult(start, end, column, sortdesc)
    count = len(results)

    return jsonify({
        "data": addUserLinks(results),
        "links": genLinks("/users/", page, pages, limit),
        "paging": genPagingInfo(total, limit, pages, count, page),
        "sort": {
            "sortby": column,
            "sortdesc": sortdesc
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


@user.route('/', methods=['POST'])
def create():
    form = UserForm(request.form)
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
            "links": [
                link("/users/%s/time" % newUser.getPK(), "time", "GET"),
                link("/users/", "listing", "GET")
            ]
        }), 201

    return jsonify({"errors": form.errors.items()}), 400


@user.route('/<string:pk>', methods=['PUT'])
def update(pk):
    try:
        user = users.getUser(pk=pk)
        form = UserForm(request.form)
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
                "links": [
                    link("/users/%s/time" % user.getPK(), "time", "GET"),
                    link("/users/", "listing", "GET")
                ]
            }), 200
        return jsonify({"errors": form.errors.items()}), 400
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
