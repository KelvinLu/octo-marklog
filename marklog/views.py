import os, json

from jinja2 import Environment, PackageLoader

from marklog import app
from marklog import posts



def index():
    env = Environment(loader=PackageLoader('marklog', 'templates'))
    listings_template = env.get_template('index.html')

    context = {

    }

    return listings_template.render(**context)



def listings(page = 1):
    limit = 15
    offset = (page - 1) * limit
    postquery = posts.Post.query.order_by(posts.Post.postdate.desc()).offset(offset).limit(limit).all()

    if (not postquery) and offset:
        return None

    listings = [{
        "slug": post.slug,
        "title": post.title,
        "previewtext": post.previewtext,
        "previewimage": post.previewimage,
        "postdate": post.postdate.strftime("%d %B, %Y"),
    } for post in postquery]
    

    return listings
