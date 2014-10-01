fakemd = """Title: My {0}th Post
PreviewText: This is my {0}th post!
PreviewImage: http://confrazzled.com/wp-content/uploads/2014/08/cat2.jpg

An h1 header
============

This is post {0}
"""

for i in range(4, 30):
	f = open("my_" + str(i) + "th_post.md", 'w')
	f.write(fakemd.format(str(i)))
	f.close()