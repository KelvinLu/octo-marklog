import os

from marklog import app
from marklog import posts
from marklog import views

# Update database of articles and render each post content's HTML into /post
posts.Post.update_files()

# Generate index page
html = views.listings(1)

html_f = open(os.path.join(app.config['GITHUB_BASE_DIR'], 'index.html'), 'w')
html_f.write(html)
html_f.close()

# Generate 404 page
html = views.error_404()

html_f = open(os.path.join(app.config['GITHUB_BASE_DIR'], '404.html'), 'w')
html_f.write(html)
html_f.close()

# Generate all listing pages into 
page = 1
while True:
    html = views.listings(page)

    if html is None:
        break

    html_f = open(os.path.join(app.config['GITHUB_LISTINGS_DIR'], '{0}.html'.format(page)), 'w')
    html_f.write(html)
    html_f.close()

    page += 1