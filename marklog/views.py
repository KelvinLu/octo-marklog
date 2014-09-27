from marklog import app
from marklog import blogapp

@app.route('/')
def index():
	return 'Hello World!'

@app.route('/ajax/listings')
def listings():
	return 'Hello World!'

@app.route('/post/<postslug>')
def blogpost():
	return 'Hello World!'