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