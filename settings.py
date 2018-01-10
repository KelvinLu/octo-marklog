import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

BASE_DIR =      basedir
ASSETS_PATH =   'assets'

POST_DIR =      os.path.join(basedir, 'post')
LISTINGS_DIR =  os.path.join(basedir, 'listings')
MARKDOWN_DIR =  os.path.join(basedir, 'markdown')

BLOG_TITLE =    'My Awesome Marklog Blog'
BLOG_DESC =     'I am very cool'
