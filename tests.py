# -*- coding: utf-8 -*-

import os
import unittest

# Setup testing environment variables
os.environ['ENVIRONMENT'] = "test"
os.environ['TOKEN'] = "test"

# Import kindlr application
import app

class AppTestCase(unittest.TestCase):
	def setUp(self):
		self.app = app.app.test_client()

	def tearDown(self):
		pass

	def test_environment(self):
		assert app.environment() == 'test', "environment should be test"

	def test_authenticate(self):
		assert app.authenticate(os.getenv('TOKEN'))

if __name__ == "__main__":
	unittest.main()
