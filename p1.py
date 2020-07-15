import sys
import time
import random as rand
import math

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


class Process:
	def __init__(self, name, cpu_time, io_time, state, turn_time, wait_time):
		self.n = name
		self.cpu = cpu_time
		self.io = io_time
		self.s = state
		self.turn = turn_time
		self.wait = wait_time
	def getName():
		return self.n
	def setName(name):
		self.n = name
	def getCpu():
		return self.cpu
	def setCpu(cpu_time):
		self.cpu = cpu_time
	def getIo():
		return self.io
	def setIo(io_time):
		self.io = io_time
	def getState():
		return self.s
	def setState(state):
		self.s = state

def burstnumber(input):
	input = input * 100
	input = math.trunc(input)
	input += 1
	return input
    
if __name__ == "__main__":
	inputlen = len(sys.argv)
	if (not(inputlen == 9 or inputlen == 8)):
	    #make the code fucking stop here
		print("bad args")
	numpros = sys.argv[1]
	seed = sys.argv[2]
	l = sys.argv[3]
	expceil = sys.argv[4]
	switchtime = sys.argv[5]
	alpha = sys.argv[6]
	tslice = sys.argv[7]
	rradd = "END"  # end
	#check if the optional one is added
	if (inputlen == 9):
		print(sys.argv[8])
		if (sys.argv[8] == "END"):
			rradd = "END"
		elif (sys.argv[8] == "BEGINNING"):
			rradd = "Beginning"
		else:
			print("invalid arg 8")
			print("Testing")
			r = rand.random()
			print(r)
			
			
	bursttest = 0.0856756876765
	bursttest = burstnumber(bursttest)
	print(bursttest, "This should be 9")
	min = 0
	max = 0
	sum = 0
	#replace l with argv[3]
	#replace upperbound with argv[4]
	iterations = 10000000
	l = 0.001
	upperbound = 3000	
	for i in range(iterations):
	    #replace random() with drand48
		r = rand.random() #/ * uniform # dist[0.00, 1.00) -- also check out random() * /
		x = -math.log(r) / l# / lambda; / * log() is natural log * /
		# / * avoid values that are far down the "long tail" of the distribution * /
		if (x > upperbound):
			i -= 1
			continue
		if (i < 20):
			print("x is ", x)
		sum += x
		if (i == 0 or x < min):
			min = x
		if ( i == 0 or x > max ):
			max = x
	    
		avg = sum / iterations
		print( "minimum value: ", min)
		print( "maximum value: ", max)
		print( "average value: ", avg)	
	s = 'A'
	##Run through the process, creating one for each s
	randy = rand(int(seed));
	for pro in range(int(numpros)):
		print(s)
		randy.srand48(randy.n);
		cpu_time = randy.drand48();
	    #process(s, )
		s = chr(ord(s) + 1)
	
	
	print(sys.argv[2])