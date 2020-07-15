import sys
import math
import random

class rand:
	def __init__(self,seed):
		self.n = seed
	def setSeed(self, seed):
		self.n = seed
	def lcg(self):
		self.n = (25214903917 * self.n + 11) & (2**48 - 1)
		return self.n
	def srand48(self, seed):
		self.n = (seed << 16) + 0x330e
	def drand48(self):
		return self.lcg() / 2**48
'''	
x = rand(1001)
x.srand48(1001)
'''
