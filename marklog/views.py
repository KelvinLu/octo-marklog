import os, json

from marklog import app
from marklog import posts



def meta():
    return {
        "blog_title": app.config['MARKLOG_BLOG_TITLE'],
        "blog_desc": app.config['MARKLOG_BLOG_DESC'],
    }



def listings(page = 1):
    limit = 15
    offset = (page - 1) * limit
    postquery = posts.Post.query.order_by(posts.Post.postdate.desc()).offset(offset).limit(limit).all()

    if (not postquery) and offset:
        return None

    listings = [{
        "slug": post.slug,
        "title": post.title,
        "preview_text": post.previewtext,
        "preview_image": post.previewimage,
        "date": post.postdate.strftime("%d %B, %Y"),
    } for post in postquery]
    

    return listings
