from marklog import app, db, cache

import os
import glob
import datetime as dt
import re
from unicodedata import normalize
import markdown



MAX_STR_LIM = 200



md = markdown.Markdown(extensions = ['markdown.extensions.meta', 
	'markdown.extensions.fenced_code',
	'markdown.extensions.smart_strong',])



# Snippet from http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.;]+')
def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word)
        if word:
            result.append(word)
    return delim.join(result)


class Post(db.Model):
	id = 			db.Column(db.Integer, primary_key = True)
	filename =		db.Column(db.String(MAX_STR_LIM))
	title = 		db.Column(db.String(MAX_STR_LIM))
	previewtext = 	db.Column(db.Text)
	previewimage = 	db.Column(db.String(MAX_STR_LIM))
	postdate =		db.Column(db.DateTime)
	filedate =		db.Column(db.DateTime)
	slug =			db.Column(db.String(MAX_STR_LIM))

	def __init__(self, filename, filepath, title, postdate, previewtext, previewimage):
		self.filename = filename
		self.title = title
		self.previewtext = previewtext
		self.previewimage = previewimage
		self.postdate = postdate
		self.filedate = dt.datetime.fromtimestamp(os.path.getmtime(filepath))

		self.slug = Post.get_slug(self.title)


	def __repr__(self):
		return '<Post: {}>'.format(self.title)

	@classmethod
	def get_slug(cls, name):
		slug = slugify(name)
		i = 0
		while cls.query.filter_by(slug = slug).all():
			i += 1
			slug = slugify(name + r'_' + str(i))
		return slug

	@classmethod
	def update_files(cls):
		filepaths = glob.glob(os.path.join(app.config['MARKLOG_POST_DIR'], '*.md'))
		filenames = list(map(os.path.basename, filepaths))
		files = zip(filenames, filepaths)

		# 1. Prune Posts that are missing from posts folder
		for post in cls.query.all():
			if post.filename not in filenames:
				db.session.delete(post)

		db.session.commit()

		# 2. Add new Post for unregistered files from posts folder
		#	 and update those that exist
		for f in files:
			post = cls.query.filter_by(filename = f[0]).first()
			if post:
				file_mod_date = dt.datetime.fromtimestamp(os.path.getmtime(f[1]))
				if post.filedate < file_mod_date:
					db.session.delete(post)
					db.session.commit()
				else:
					continue
			post, html = cls.new_post(f[0], f[1])
			cache.set(post.slug, html)
			if post:
				db.session.add(post)

		db.session.commit()

	@classmethod
	def new_post(cls, filename, filepath):
		# Since filenames are already computed, we'll just use those again
		f = open(filepath, 'r')
		html = md.reset().convert(f.read())
		f.close()
		# TODO: ensure no string field is over the global char limit
		title = md.Meta.get('title', [''])[0]
		date = md.Meta.get('date', [''])[0]
		previewtext = md.Meta.get('previewtext', [''])[0]		
		previewimage = md.Meta.get('previewimage', [''])[0]

		if not title:
			return False

		try:
			year, month, day = map(int, date.split('-'))
			postdate = dt.datetime(year = year, month = month, day = day)
		except Exception:
			postdate = dt.datetime.fromtimestamp(os.path.getctime(filepath))

		return cls(filename, filepath, title, postdate, previewtext, previewimage), html

	def render_html(self):
		filepath = os.path.join(app.config['MARKLOG_POST_DIR'], self.filename)
		html = cache.get(self.slug)

		if html:
			return html

		f = open(filepath, 'r')
		html = md.reset().convert(f.read())
		f.close()

		cache.set(self.slug, html)

		return html