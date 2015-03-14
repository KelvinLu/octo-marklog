from flask import request, Response, json, abort, render_template, url_for, jsonify
from jinja2 import Environment, PackageLoader

from marklog import app
from marklog import posts

import os

env = Environment(loader=PackageLoader('marklog', 'templates'))
listings_template = env.get_template('listings.html')
post_template = env.get_template('post.html')
notfound_template = env.get_template('404.html')


def listings(page = 1):
    limit = 15
    offset = (page - 1) * limit
    postquery = posts.Post.query.order_by(posts.Post.postdate.desc()).offset(offset).limit(limit).all()

    if (not postquery) and offset:
        return None

    context = {
        "blog_title": app.config['MARKLOG_BLOG_TITLE'],
        "blog_desc": app.config['MARKLOG_BLOG_DESC'],
        "post_colors": app.config['MARKLOG_BLOG_POST_COLORS'],
        "posts": postquery,
        "nextpage": page + 1,
        "prevpage": page - 1,
    }
    return listings_template.render(**context)

def blogpost(post):
    context = {
        "blog_title": app.config['MARKLOG_BLOG_TITLE'],
        "post_title": post.title,
        "post_html": post.render_html(),
    }

    return jsonify(**context)

def error_404(e = None):
    context = {
        "blog_title": app.config['MARKLOG_BLOG_TITLE'],
        "post_colors": app.config['MARKLOG_BLOG_POST_COLORS'],
    }

    return notfound_template.render(**context)