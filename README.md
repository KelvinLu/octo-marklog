Marklog
=======

![Travis](https://travis-ci.org/KelvinLu/marklog.svg?branch=master)

> *Someone please tell me why pip returns with an exit code of 1 when run on Travis*

Serve static Markdown files as articles. All the cool kids have blogs.

## Running a demo

Unfortunately, I do not have a demo set up online. If you want to see Marklog in action, please run it on your local machine!

Setting it up requires minimal work:

1. Clone the repo
2. Use pip to install dependencies, either in a virtualenv or not
3. Run `fakeposts.py` in `marklog/assets/posts` to generate some fake posts
4. Run `updateposts.py` in the project root to update the listing database
5. Run `runserver.py`
6. Visit `http://localhost:5000`

```bash
git clone https://github.com/KelvinLu/marklog
cd marklog
pip install -r requirements.txt
cd marklog/assets/posts
python fakeposts.py 40
cd ../../../
python updateposts.py
python runserver.py
```
