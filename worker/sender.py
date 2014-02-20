# -*- coding: utf-8 -*-

import os
import sys
import time

class Sender:
	"""The sender class"""

	def __init__(self, config=None, parser=None):
		"""Class init"""
		self._config = config
		self._parser = parser

	def process(self, url):
		"""Process a URL for sending"""
		pass

	def _send(self):
		"""Send a generated mobi to an email address"""
		pass
