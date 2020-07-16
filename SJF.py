import sys
import time
import random as rand
import math


class rand:
    def __init__(self, seed):
        self.n = seed

    def setSeed(self, seed):
        self.n = seed

    def lcg(self):
        self.n = (25214903917 * self.n + 11) & (2 ** 48 - 1)
        return self.n

    def srand48(self, seed):
        self.n = (seed << 16) + 0x330e

    def drand48(self):
        return self.lcg() / 2 ** 48


class Process:
    def __init__(self, name, cpu_time, io_time, state, num_burst, arrival_time, turn_time, wait_time):
        self.n = name
        self.cpu = cpu_time
        self.io = io_time
        self.s = state
        self.b = num_burst
        self.a = arrival_time
        self.turn = turn_time
        self.wait = wait_time

    def getName(self):
        return self.n

    def setName(self, name):
        self.n = name

    def getCpu(self):
        return self.cpu

    def setCpu(self, cpu_time):
        self.cpu = cpu_time

    def getIo(self):
        return self.io

    def setIo(self, io_time):
        self.io = io_time

    def getState(self):
        return self.s

    def setState(self, state):
        self.s = state

    def getBurst(self):
        return self.b

    def setBurst(self, num_burst):
        self.b = num_burst

    def setArrival(self, arrival_time):
        self.a = arrival_time

    def getArrival(self):
        return self.a






def SJF(listp, tcs, alpha,lambdainput):
    time = 0
    for pid in range(len(listp)):
        print("process", (listp[pid].a))
    newlist = []
    newlist = sorted(listp, key=lambda x: x.getArrival())
    time += (tcs/2)
    tau = 1/lambdainput
    for pid in range(len(newlist)):
        tau = math.ceil(alpha * burst_io_time[processName][0] + (1 - alpha) * tau
        print("process2",(newlist[pid].a))











def burstnumber(input):
    input = input * 100
    input = math.trunc(input)
    input += 1
    return input


if __name__ == "__main__":
    inputlen = len(sys.argv)
    if (not (inputlen == 9 or inputlen == 8)):
        # make the code fucking stop here
        print("bad args")

    numpros = int(sys.argv[1])
    seed = sys.argv[2]
    l = sys.argv[3]
    expceil = sys.argv[4]
    switchtime = int(sys.argv[5])
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



    # bursttest = 0.0856756876765
    # bursttest = burstnumber(bursttest)
    # print(bursttest, "This should be 9")

    # replace l with argv[3]
    # replace upperbound with argv[4]
    min = 0
    max = 0
    sum = 0
    iterations = 1000000
    l = 0.001
    upperbound = 3000
    interarrival = []
    randy = rand(1001)
    randy.srand48(1001)
    for i in range(iterations):
        # replace random() with drand48
        r = randy.drand48()  # / * uniform # dist[0.00, 1.00) -- also check out random() * /
        x = -math.log(r) / l  # / lambda; / * log() is natural log * /
        # / * avoid values that are far down the "long tail" of the distribution * /
        if (x > upperbound):
            i -= 1
            continue
            # print("x is ", x)
        interarrival.append(x)
        sum += x
        if (i == 0 or x < min):
            min = x
        if (i == 0 or x > max):
            max = x

        avg = sum / iterations
        # print( "minimum value: ", min)
        # print( "maximum value: ", max)
        # print( "average value: ", avg)

    process_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                     'U', 'V', 'W', 'X', 'Y', 'Z']
    plist_RR = []
    plist_SRT = []
    plist_SJF = []
    plist_FCFS = []

    # fill each list with default processes
    for i in range(numpros):
        plist_RR.append(Process(process_names[i], 0, 0, 1, 0, 0, 0,
                                0))  # Adds process into the list, all times set to 0 and default state of 1
        plist_SJF.append(Process(process_names[i], 0, 0, 1, 0, 0, 0, 0))
        plist_SRT.append(Process(process_names[i], 0, 0, 1, 0, 0, 0, 0))
        plist_FCFS.append(Process(process_names[i], 0, 0, 1, 0, 0, 0, 0))
    # DO calculations to give proceses their rime values.
    rand_index = 0;
    for p in plist_RR:
        p.setArrival((math.floor(10.64899)))
        rand_index += 1
        temp_num_burst = burstnumber(interarrival[rand_index])
        p.setBurst(temp_num_burst)
        rand_index += 1
        for r in range(temp_num_burst):
            p.setCpu(math.ceil(interarrival[rand_index]))
            rand_index += 1
            if (r == temp_num_burst - 1):
                break
            p.setIo(math.ceil(interarrival[rand_index]))
            rand_index += 1

    rand_index = 0
    for p in plist_SRT:
        p.setArrival(math.floor(interarrival[rand_index]))
        rand_index += 1
        temp_num_burst = burstnumber(interarrival[rand_index])
        p.setBurst(temp_num_burst)
        rand_index += 1
        for r in range(temp_num_burst):
            p.setCpu(math.ceil(interarrival[rand_index]))
            rand_index += 1
            if (r == temp_num_burst - 1):
                break
            p.setIo(math.ceil(interarrival[rand_index]))
            rand_index += 1

    rand_index = 0
    for p in plist_SJF:
        p.setArrival(math.floor(interarrival[rand_index]))
        rand_index += 1
        temp_num_burst = burstnumber(interarrival[rand_index])
        p.setBurst(temp_num_burst)
        rand_index += 1
        for r in range(temp_num_burst):
            p.setCpu(math.ceil(interarrival[rand_index]))
            rand_index += 1
            if (r == temp_num_burst - 1):
                break
            p.setIo(math.ceil(interarrival[rand_index]))
            rand_index += 1

    rand_index = 0
    for p in plist_FCFS:
        p.setArrival(math.floor(interarrival[rand_index]))
        rand_index += 1
        temp_num_burst = burstnumber(interarrival[rand_index])
        p.setBurst(temp_num_burst)
        rand_index += 1
        for r in range(temp_num_burst):
            p.setCpu(math.ceil(interarrival[rand_index]))
            rand_index += 1
            if (r == temp_num_burst - 1):
                break
            p.setIo(math.ceil(interarrival[rand_index]))
            rand_index += 1
    SJF(plist_SJF, switchtime, alpha)