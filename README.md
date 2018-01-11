Octo-Marklog
=======

Serve static Markdown files as articles... on GitHub! All the cool kids have GitHubs.

This is an offshoot of the original [Marklog](https://github.com/KelvinLu/marklog) project.

It's meant to be run on GitHub's generously provided personal sites. Simply clone this repo, do the Marklog thing, change to upstream to your `<username>.github.io` repo, and push!

Want to demo it locally first? No problem.

1. Clone or submodule the `octo-marklog` repository into an empty directory.
2. Run `./octo-marklog/bootstrap`, within the directory.
3. Activate the `virtualenv` (bootstrapped within `env`).
4. Run `./octo-marklog/fakeposts`, within the directory.
5. Run `./octo-marklog/updateblog`, within the directory.
6. Run Python's built-in development server.
7. Visit `http://localhost:8000`.

```bash
# within an empty directory

git clone https://github.com/KelvinLu/octo-marklog

./octo-marklog/bootstrap
./env/bin/python ./octo-marklog/fakeposts 5
./env/bin/python ./octo-marklog/updateblog

python -m SimpleHTTPServer
```
