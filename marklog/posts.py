import sys
import os
import fnmatch
import glob
import itertools
import datetime as dt
import re
from unicodedata import normalize
import markdown
import json

from pyembed.markdown import PyEmbedMarkdown

from marklog import app, db
from marklog import compat, marklog_ext



MAX_STR_LIM = 200



MARKLOG_EXT = marklog_ext.MarklogExtension()
md = markdown.Markdown(extensions = ['markdown.extensions.meta',
    'markdown.extensions.fenced_code',
    'markdown.extensions.smart_strong',
    PyEmbedMarkdown(),
    MARKLOG_EXT,])



# Snippet from http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.;]+')
def slugify(text, delim=u'-'):
    """Generates a slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word)
        if word:
            result.append(word)
    return delim.join(result)



if compat.PY_VERSION == 2:
    to_unicode = lambda text: unicode(text, 'utf-8')
else:
    to_unicode = lambda text: text




def markdown_convert(filepath):
    f = open(filepath, 'r')
    MARKLOG_EXT.setConfig('marklog_file_hint', filepath)
    html = md.reset().convert(to_unicode(f.read()))
    f.close()

    return html, md.Meta



class Post(db.Model):
    id =            db.Column(db.Integer, primary_key = True)
    filepath =      db.Column(db.String(MAX_STR_LIM))
    title =         db.Column(db.String(MAX_STR_LIM))
    previewtext =   db.Column(db.Text)
    previewimage =  db.Column(db.String(MAX_STR_LIM))
    postdate =      db.Column(db.DateTime)
    filedate =      db.Column(db.DateTime)
    slug =          db.Column(db.String(MAX_STR_LIM))

    def __init__(self, filepath, fullpath, title, postdate, previewtext, previewimage):
        self.filepath = filepath
        self.title = title
        self.previewtext = previewtext
        self.previewimage = previewimage
        self.postdate = postdate
        self.filedate = dt.datetime.fromtimestamp(os.path.getmtime(fullpath))

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
        markdown_dir = app.config['MARKDOWN_DIR']

        files = []
        for root, dirname, filename in os.walk(markdown_dir):
            for filename in filename:
                path = os.path.join(root, filename)
                if fnmatch.fnmatch(path, '*.md') and os.access(path, os.R_OK):
                    files.append([os.path.normpath(path).replace(os.path.normpath(markdown_dir) + os.path.sep, '', 1), path])

        # 1. Prune Posts that are missing from posts folder
        for post in cls.query.all():
            if post.filepath not in itertools.imap(lambda x: x[0], files):
                os.remove(os.path.join(app.config['POST_DIR'], '{0}.json'.format(post.slug)))
                db.session.delete(post)

        db.session.commit()

        # 2. Add new Post for unregistered files from posts folder
        #    and update those that exist
        for filepath, fullpath in files:
            post = cls.query.filter_by(filepath = filepath).first()
            if post:
                file_mod_date = dt.datetime.fromtimestamp(os.path.getmtime(fullpath))
                if post.filedate < file_mod_date:
                    db.session.delete(post)
                    db.session.commit()
                else:
                    continue
            post, html = cls.new_post(filepath, fullpath)

            if post:
                context = {
                    "post_title": post.title,
                    "post_html": html,
                }

                f = open(os.path.join(app.config['POST_DIR'], '{0}.json'.format(post.slug)), 'w')
                f.write(json.dumps(context))
                f.close()

                db.session.add(post)

        db.session.commit()

    @classmethod
    def new_post(cls, filepath, fullpath):
        html, meta = markdown_convert(fullpath)

        # TODO: ensure no string field is over the global char limit
        title = meta.get('title', [''])[0]
        date = meta.get('date', [''])[0]
        previewtext = meta.get('previewtext', [''])[0]
        previewimage = meta.get('previewimage', [''])[0]

        if not title:
            return False, None

        try:
            year, month, day = map(int, date.split('-'))
            postdate = dt.datetime(year = year, month = month, day = day)
        except Exception:
            postdate = dt.datetime.fromtimestamp(os.path.getctime(filepath))

        return cls(filepath, fullpath, title, postdate, previewtext, previewimage), html
