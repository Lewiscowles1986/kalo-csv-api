from hateoas.link import link


def userHateoasLinks(user):
    return [
        link("/users/%s/time" % user.getPK(), "time", "GET"),
        link("/users/", "listing", "GET")
    ]