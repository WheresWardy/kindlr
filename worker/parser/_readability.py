# -*- coding: utf-8 -*-

import re
import json

import requests
from _response import ParserResponse

class Parser:
	"""Parser API implementation of Readability"""
	Name = 'Readability'
	Version = '1.0.0'
	Endpoint = 'https://www.readability.com/api/content/v1/parser'

	def __init__(self, config):
		"""Initialise the parser"""
		self._config = config

	def retrieve(self, url):
		"""Public method to retrieve content for an article URL"""
		request = requests.get(Parser.Endpoint, params={'token': self._config.readability.token, 'url': url})
		article = json.loads(request.text)
		response = ParserResponse()

		if 'error' in article:
			response.error = "Readability parser error: %s" % (article['messages'])

		if 'content' in article:
			response.content = article['content']

		if self._config.strip_images:
			response.content = re.sub('<img [^<]+?>', '', response.content)

		if not response.content:
			response.error = "Parser could not get content for URL '%s'" % (url)

		return response
