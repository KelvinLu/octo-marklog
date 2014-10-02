from flask import request, Response, json, abort, render_template, url_for

from marklog import app
from marklog import posts

import os

@app.route('/')
@app.route('/listings/<int:page>')
def listings(page = 1):
	limit = 15
	offset = (page - 1) * limit
	postquery = posts.Post.query.order_by(posts.Post.postdate.desc()).offset(offset).limit(limit).all()

	if not postquery:
		abort(404)

	context = {
		"blog_title": app.config['MARKLOG_BLOG_TITLE'],
		"blog_desc": app.config['MARKLOG_BLOG_DESC'],
		"posts": postquery,
		"nextpage": page + 1,
		"prevpage": page - 1,
	}
	return render_template('listings.html', **context)

@app.route('/update')
def update():
	posts.Post.update_files()
	return str(posts.Post.query.all())

@app.route('/post/<postslug>')
def blogpost(postslug):
	p = posts.Post.query.filter_by(slug = postslug).first()
	if not p:
		abort(404)

	return p.render_html()