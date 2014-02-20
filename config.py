# -*- coding: utf-8 -*-

import os

class Config:
	"""Hold configuration for kindlr"""

	def __init__(self):
		"""Initialise configuration defaults"""
		self.environment = os.getenv('ENVIRONMENT', 'production')
		self.parser = os.getenv('PARSER', 'newspaper')
		self.token = os.getenv('TOKEN', '')
		self.strip_images = os.getenv('STRIP_IMAGES', False)

		self.readability = Readability()

class Readability:
	"""Hold sub-configuration for Readability"""

	def __init__(self):
		"""Initialise configuration defaults"""
		self.token = os.getenv('READABILITY_TOKEN', '')
