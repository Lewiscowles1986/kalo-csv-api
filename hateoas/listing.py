from .link import link


def genPagingInfo(total, limit, pages, count, page):
    """Generate information to inform consumers of listing request state"""
    return {
        "total": total,
        "limit": limit,
        "pages": pages,
        "count": count,
        "page": page
    }


def genLinks(basePath, page, pages, limit):
    """Generate pagination links for HATEOAS listing"""
    links = []

    links.append(link(linkUri(basePath, 1, limit), "first", "GET"))
    if page > 1:
        links.append(link(linkUri(basePath, page - 1, limit), "prev", "GET"))
    links.append(link(linkUri(basePath, page, limit), "current", "GET"))
    if page < pages:
        links.append(link(linkUri(basePath, page + 1, limit), "next", "GET"))
    links.append(link(linkUri(basePath, pages, limit), "last", "GET"))

    return links


def linkUri(basePath, page, limit):
    """Generate link URI for HATEOAS listing"""
    return "{}?page={}&limit={}".format(basePath, page, limit)
