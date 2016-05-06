# -*- coding: utf-8 -*-

import os
import sys
import time
import threading

from config import Config
from bucket import Bucket
from worker.sender import Sender
from flask import Flask, render_template, request, abort

# Create configuration
config = Config()

# Create the request rate limiter
bucket = Bucket()

# Create the chosen URL parser
if config.parser == 'readability':
	from worker.parser._readability import Parser
else:
	from worker.parser._newspaper import Parser

parser = Parser(config)

# Flask application
app = Flask(__name__)

# Environment-based options
if config.environment == "development":
	app.debug = True
elif config.environment == "test":
	app.testing = True

# Write errors to stderr
def stderr(message):
	sys.stderr.write(message + "\n")

# Return the current environment
def environment():
	return config.environment

# Authenticate a request against the environment token
def authenticate(token):
	if config.token == "" or token != config.token:
		stderr("Token empty or invalid")
		abort(403)
	else:
		return True

# Check if a request needs rate limiting
def limit():
	if bucket.limit(request.remote_addr):
		stderr("Request was rate limited")
		abort(403)
	else:
		return False

@app.route('/')
def index():
	return render_template('index.html.jinja')

@app.route('/send/<token>/<path:url>')
def send(token=None, url=None):
	limit()
	authenticate(token)

	s = Sender(config, parser)
	threading.Thread(target=s.process, args=[url]).start()
	return render_template('send.html.jinja')

@app.route('/preview/<token>/<path:url>')
def preview(token=None, url=None):
	limit()
	authenticate(token)

	try:
		article = parser.retrieve(url)
		status = 200
	except:
		article = "Could not retrieve resource for URL '%s' (parser: %s)" % (url, config.parser)
		status = 400

	if article.error:
		content = article.error
	else:
		content = article.content

	print(article.content)

	return render_template('preview.html.jinja', article=content), status

@app.route('/calibre/')
def calibre():
	os.system("calibre/ebook-convert")
	
	return "calibre"

if __name__ == "__main__":
	app.run(port=8080)
