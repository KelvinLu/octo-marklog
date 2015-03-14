import os
import json

from marklog import app
from marklog import posts
from marklog import views

# Update database of articles and render each post content's HTML into /post
posts.Post.update_files()

# Generate meta info
meta = views.meta()

f = open(os.path.join(app.config['GITHUB_BASE_DIR'], 'meta.json'), 'w')
f.write(json.dumps(meta))
f.close()

# Generate all listing pages into 
page = 1
while True:
    listings = views.listings(page)

    if listings is None:
        break

    f = open(os.path.join(app.config['GITHUB_LISTINGS_DIR'], '{0}.json'.format(page)), 'w')
    f.write(json.dumps(listings))
    f.close()

    page += 1