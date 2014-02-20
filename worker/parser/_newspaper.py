# -*- coding: utf-8 -*-

import re

import requests
from _response import ParserResponse
from bs4 import BeautifulSoup
from newspaper import Article

class Parser:
	"""Parser API implementation of Newspaper"""
	Name = 'Newspaper'
	Version = '1.0.0'
	Endpoint = None

	def __init__(self, config):
		"""Initialise the parser"""
		self._config = config

	def retrieve(self, url):
		"""Public method to retrieve content for an article URL"""
		pages = self._pages(url)
		response = ParserResponse()

		for page in pages:
			article = Article(page, keep_article_html=True)
			article.download()
			article.parse()
			response.content = response.content + article.article_html

		if self._config.strip_images:
			response.content = re.sub('<img [^<]+?>', '', response.content)

		if not response.content:
			response.error = "Parser could not get content for URL '%s'" % (url)

		return response

	def _pages(self, url):
		"""Use _pagination to return a list of article pages for the URL"""
		request = requests.get(url)
		content = BeautifulSoup(request.text, "html5lib")

		return [url] + self._pagination(content)

	def _pagination(self, content):
		"""Attempt to detect pagination from the source"""
		pages = []

		# Ars Technica
		for nav in content.find_all(re.compile("nav")):
			try:
				if 'page-numbers' in nav['class']:
					for pagenumbers in nav.find_all('a'):
						if re.match('^[0-9]+$', pagenumbers.text):
							pages.append(pagenumbers.attrs['href'])
			except KeyError:
				pass

		return pages
