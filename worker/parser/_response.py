# -*- coding: utf-8 -*-

class ParserResponse:
	"""Response format for a Parser API request"""

	def __init__(self):
		self.content = ""
		self.error = ""
		self.author = ""
		self.url = ""
