class Process:
    def __init__(self, name, cpu_time, io_time, state):
        self.n = name
        self.cpu = cpu_time
        self.io = io_time
        self.s = state