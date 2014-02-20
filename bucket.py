# -*- coding: utf-8 -*-

import time

class Bucket:
	def __init__(self, rate = 1.0, time = 1.0):
		self.rate = rate
		self.time = time
		self.allowance = {}
		self.check = {}

	def limit(self, address):
		if address not in self.allowance:
			self.check[address] = time.time()
			self.allowance[address] = self.rate

		time_current = time.time()
		time_passed = (time_current - self.check[address])
		self.check[address] = time_current
		self.allowance[address] = (self.allowance[address] + (time_passed * (self.rate / self.time)))

		# Allow the request
		if self.allowance[address] >= 1.0:
			self.allowance[address] = (self.allowance[address] - 1)
			return False
		# Deny the request
		else:
			return True
