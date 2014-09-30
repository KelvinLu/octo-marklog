from flask import request, Response, json, abort, render_template, url_for

from marklog import app
from marklog import posts

import os

@app.route('/')
def index():
	context = {
		"blog_title": app.config['MARKLOG_BLOG_TITLE']
	}
	return render_template('base.html', **context)

@app.route('/update')
def update():
	posts.Post.update_files()
	return str(posts.Post.query.all())

@app.route('/ajax/listings')
def listings():
	offset = request.args.get('offset', 0, type = int)
	limit = request.args.get('limit', 10, type = int)
	q = posts.Post.query.order_by(posts.Post.postdate.desc()).offset(offset).limit(limit).all()
	results = [{
				"title": post.title, 
				"previewtext": post.previewtext,
				"previewimage": post.previewimage,
				"postdate": post.postdate,
				"slug": post.slug,
	} for post in q]

	return Response(json.dumps(results), mimetype = 'application/json')


@app.route('/post/<postslug>')
def blogpost(postslug):
	p = posts.Post.query.filter_by(slug = postslug).first()
	if not p:
		abort(404)

	return p.render_html()