Octo-Marklog
=======

Serve static Markdown files as articles... on GitHub! All the cool kids have GitHubs.

This is an offshoot of the original [Marklog](https://github.com/KelvinLu/marklog) project.

It's meant to be run on GitHub's generously provided personal sites. Simply clone this repo, do the Marklog thing, change to upstream to your *username*.github.io repo, and push!

Want to demo it yourself locally?

1. Clone the repo
2. Use pip to install dependencies, either in a virtualenv or not
3. Run `fakeposts.py` in `marklog/assets/posts` to generate some fake posts
4. Run `updateposts.py` in the project root to update the listing database
5. Run Python's built-in development server
6. Visit `http://localhost:8000`

```bash
git clone https://github.com/KelvinLu/octo-marklog
cd octo-marklog
pip install -r requirements.txt
cd marklog/assets/posts
python fakeposts.py 40
cd ../../../
python updateposts.py
python -m SimpleHTTPServer
```
