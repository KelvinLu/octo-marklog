from flask import request, Response, json, abort, render_template, url_for

from marklog import app
from marklog import posts

import os

def listings(page = 1):
    limit = 15
    offset = (page - 1) * limit
    postquery = posts.Post.query.order_by(posts.Post.postdate.desc()).offset(offset).limit(limit).all()

    if (not postquery) and offset:
        abort(404)

    context = {
        "blog_title": app.config['MARKLOG_BLOG_TITLE'],
        "blog_desc": app.config['MARKLOG_BLOG_DESC'],
        "post_colors": app.config['MARKLOG_BLOG_POST_COLORS'],
        "posts": postquery,
        "nextpage": page + 1,
        "prevpage": page - 1,
    }
    return render_template('listings.html', **context)

def blogpost(postslug):
    p = posts.Post.query.filter_by(slug = postslug).first()

    if not p:
        abort(404)

    html = p.render_html()

    context = {
        "blog_title": app.config['MARKLOG_BLOG_TITLE'],
        "post_title": p.title,
        "post_html": p.render_html(),
    }

    return render_template('post.html', **context)

def error_404(e = None):
    context = {
        "blog_title": app.config['MARKLOG_BLOG_TITLE'],
        "post_colors": app.config['MARKLOG_BLOG_POST_COLORS'],
    }

    return render_template('404.html', **context), 404

def error_500(e = None):
    context = {
        "blog_title": app.config['MARKLOG_BLOG_TITLE'],
        "post_colors": app.config['MARKLOG_BLOG_POST_COLORS'],
    }

    return render_template('500.html', **context), 500