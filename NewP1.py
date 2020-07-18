import sys
import time
import random as rand
import math
import queue
import heapq

process_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                     'U', 'V', 'W', 'X', 'Y', 'Z']

f = open('testout.txt', 'w')


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
    def __init__(self, name, cpu_times, io_times, cpu_index, io_index, num_burst, arrival_time, turn_time,
                 wait_time, input_tau, tau_array):
        self.n = name
        self.cpu = cpu_times
        self.io = io_times
        self.cpu_i = cpu_index
        self.io_i = io_index
        self.b = num_burst
        self.a = arrival_time
        self.turn = turn_time
        self.wait = wait_time
        self.tau = input_tau
        self.tauarray = tau_array

    def __lt__ (self, obj):
            """self < obj."""
            if(self.tauarray[self.cpu_i] == obj.tauarray[obj.cpu_i]):
                return self.n < obj.n
            else:
                return (self.tauarray[self.cpu_i] < obj.tauarray[obj.cpu_i])

def burstnumber(input):
    input = input * 100
    input = math.trunc(input)
    input += 1
    return input


def printNames(ready_queue):
    if (len(ready_queue) == 0):
        return "<empty>]"
    string = ""
    for p in ready_queue:
        if (ready_queue.index(p) == (len(ready_queue) - 1)):
            string += p.n + "]"
        else:
            string += p.n + " "
    return string

def loadProcesses(p_list, seed, l, upperbound, alpha):
    
    randy = rand(seed)
    randy.srand48(seed)
    corner_cancer = False

    for p in p_list:
        #arrival and burst num stuff
        corner_cancer = False
        r_small = randy.drand48()   
        r_big = -math.log(r_small) / l
        #if(p.n == "G"):
            #print("YERN",r_small,r_big, file = f)
        while(r_big > upperbound):
            r_small = randy.drand48()   
            r_big = -math.log(r_small) / l
       
        p.a = math.floor(r_big)
        
        r_small = randy.drand48()   
        r_big = -math.log(r_small) / l
        if(p.n == "G" and r_big > upperbound):
            temp_num_burst = burstnumber(r_small)
            p.b = temp_num_burst
            corner_cancer = True
        else:
            while(r_big > upperbound):
                r_small = randy.drand48()   
                r_big = -math.log(r_small) / l
            temp_num_burst = burstnumber(r_small)
            p.b = (temp_num_burst)

        while(r_big > upperbound):
            r_small = randy.drand48()   
            r_big = -math.log(r_small) / l

        #I/O and CPU bursts stuff
        for r in range(p.b):
            if(not corner_cancer):
                r_small = randy.drand48()   
                r_big = -math.log(r_small) / l
        
            while(r_big > upperbound):
                r_small = randy.drand48()   
                r_big = -math.log(r_small) / l
                
            p.cpu.append(math.ceil(r_big))

            if(r == temp_num_burst - 1):
                break
            r_small = randy.drand48()   
            r_big = -math.log(r_small) / l

            while(r_big > upperbound):
                r_small = randy.drand48()   
                r_big = -math.log(r_small) / l

            p.io.append(math.ceil(r_big))


        #tau stuff
        for i in range(p.b):
            if i == 0:
                p.tauarray.append(p.tau)
            else:
                p.tauarray.append(math.ceil(alpha * p.cpu[i-1] + (1-alpha) * p.tauarray[i-1]))

    return p_list


def randList(l, upperbound, seed):
    min = 0
    max = 0
    sum = 0
    iterations = 100000
    # l = 0.001
    r_list = []
    randy = rand(seed)
    randy.srand48(seed)
    for i in range(iterations):
        # replace random() with drand48
        r = randy.drand48()  # / * uniform # dist[0.00, 1.00) -- also check out random() * /

        x = -math.log(r) / l  # / lambda; / * log() is natural log * /
        # / * avoid values that are far down the "long tail" of the distribution * /

        if (x > upperbound):
            i -= 1
            continue
            # print("x is ", x)
        
        sum += x
        if (i == 0 or x < min):
            min = x
        if (i == 0 or x > max):
            max = x

        avg = sum / iterations

    return r_list
    # print( "minimum value: ", min)
    # print( "maximum value: ", max)
    # print( "average value: ", avg)


def roundRobin(plist_RR, t_slice, location, switchtime):
    #plist_RR -- list of processes
    #t_slice -- alloted time for CPU bursts 
    #location -- "Beginning" or "End", determines where process are pushed into the queue
    #switching = False
    #halfswitch = False
    context = False

    context_time = 0
    
    default = True
    if(location == "BEGINNING"):
        default = False


    time = 0
    target = 0
    
    if(t_slice < 1000000):
        print("Round Robin Algorithm Start")
    else:
        print("FCFS Algorithm Start")
    
    readyQ = []
    waitingQ = []
    running = []
    run_counter = 0

    for p in plist_RR:
        print("Process", p.n,"[NEW] (arrival time", p.a, "ms)",p.b, "CPU bursts")

    while(True):
        #time string
        #real time
        s_r = 'time ' + repr(time) + 'ms:'
        #context adjusted time
        #s_c = 'time ' + repr(time + context_time) + 'ms:'
        if(time == 0 and t_slice > 100000):
            print(s_r, "Simulator started for FCFS [Q",printNames(readyQ))
        elif(time == 0 and t_slice < 100000):
            print(s_r, "Simulator started for RR [Q",printNames(readyQ))
        #decrement current running process
        for p in running:
            #p.cpu[0 + c_counter[plist_RR.index(p)]] -= 1
            p.cpu[p.cpu_i] -= 1
            run_counter += 1


        #if running rpocess has finished
        for p in running:
            if(p.cpu[p.cpu_i] == 0):
                #context = True   #if(p.cpu[0 + c_counter[plist_RR.index(p)]] == 0)
                p.cpu_i += 1
                context = True
                context_time += 2
                if(time < 1000):
                    print(s_c, "Process", p.n, "completed a CPU burst;", (p.b - p.cpu_i),"bursts to go [Q",printNames(readyQ))
                    print(s_c, "Process", p.n, "switching out of CPU; will block on I/O until time " +str(time + p.io[p.io_i])+ "ms [Q", printNames(readyQ))
                if(p.cpu_i == (p.b - 1)):   
                    print(s_c,"Process", p.n, "terminated [Q", printNames(readyQ))
                    run_counter = 0
                    plist_RR.remove(p)
                    running.remove(p)
                else:
                    running.remove(p)
                    waitingQ.append(p)

        #check if the running process ran out of time
        if(run_counter == t_slice):
            #context = True
            if(time < 1000):
                print(s_c, "Time slice expired; process", running[0].n, "preempted with " + str(running[0].cpu[running[0].cpu_i]) + "ms to go [Q",printNames(readyQ))
            #if there are items in the readyQ
            if(len(readyQ) > 0):
                #switching = True
                temp_holder = running.pop(0)
                if(default):
                    readyQ.append(temp_holder)
                else:
                    readyQ.insert(0, temp_holder)
            else:
                #halfswitch = True
                run_counter = 0

        #check if any I/O has finished, and if so add to the readyQ. If not, decrement all
        for p in waitingQ:
            if(p.io[p.io_i] == 0):      #if(p.io[0 + i_counter[plist_RR.index(p)]] == 0):
                waitingQ.remove(p)
                p.io_i += 1             #i_counter[plist_RR.index(p)] += 1
                if(default):
                    readyQ.append(p)
                else:
                    readyQ.insert(0, p)
                if(time < 1000):
                    print(s_r, "Process", p.n, "completed I/O; added to the ready queue [Q", printNames(readyQ))
            else:
                p.io[p.io_i] -= 1             #p.io[0 + i_counter[plist_RR.index(p)]] -= 1

        #check if any processes arrive
        for p in plist_RR:
            if(p.a == time):
                #print("CPU times", p.cpu)
                #print("I/O times", p.io)
                if(default):
                    readyQ.append(p)
                else:
                    readyQ.insert(0, p)
                if(time < 1000):
                    print(s_r, "Process", p.n, "arrived; added to the ready queue [Q",printNames(readyQ))
       
        #check if nothing is running
        for p in readyQ:
            if(len(running) == 0):
                #halfswitch = True
                running.append(p)
                context = True
                context_time += int(switchtime/2)
                s_c = 'time ' + repr(time + context_time) + 'ms:'
                readyQ.remove(p)
                run_counter = 0
                if(time < 1000):
                        print(s_c, "Process", p.n, "started using the CPU for " + str(p.cpu[p.cpu_i]) +  "ms burst [Q",printNames(readyQ))                   

        #check if the running process finished
        

        


       

            #end of if context switch statement

        
        
        '''
        if(switching):
            if(halfswtich):
                target = time + (switchtime/2)
            else:
                target = time + switchtime
            if(time == target):
                swithcing = False
                halfswtich = False
        
        
        if(time > 240 and time < 245):
            print("context:", context)
            print("Half:", halfswitch)
            print("switch:", switching)
        

        if(halfswitch):
            target = time + (switchtime/2)
            #print("HALF", target)
            context = True
        if(switching):
            target = time + switchtime
            #print("REGULAR", target)
            context = True

        switching = False
        halfswitch = False

        if(time == target):
            context = False
        '''
        
        time += 1

        if(len(plist_RR) == 0):
            if(t_slice > 100000):
                print(s_c, "Simulator ended for FCFS [Q",printNames(readyQ))
                print()
            else:
                print(s_c, "Simulator ended for RR [Q",printNames(readyQ))
                print()
            break
    #end of RoundRobin


def SJF(plist_SJF, preempt, location, switchtime):
    switching = False
    halfswitch = False
    if switching:
        print("relax")
    time = 0
    target = 0
    readyQ = []
    readyQ.append(plist_SJF[0])
    heapq.heapify(readyQ)
    heapq.heappop(readyQ)
    print("arrived")
    waitingQ = []
    running = []
    run_counter = 0
    for p in plist_SJF:
        print("Process", p.n, "[NEW] (arrival time", p.a, "ms) ", p.b, "CPU bursts")
    while True:
        if time % 10000 == 0:
            print(time)
        if time == 100000:
            break
        # time string
        s = 'time ' + repr(time) + ':ms'
        if (time == 0 and not(preempt)):
            print(s, "Simulator started for SJF [Q", printNames(readyQ))
        elif(time == 0 and preempt):
            print(s, "Simulator started for SRTF [Q", printNames(readyQ))
        # context switch
        if (not switching):
            # decrement the running process, does nothing if there is no running process
            for p in running:
                p.cpu[p.cpu_i] -= 1
                run_counter += 1
            # check if the running process finished
            for p in running:
                if (p.cpu[p.cpu_i] == 0):
                    switching = True
                    p.cpu_i += 1
                    if (time < 2000):
                        print(s, "Process", p.n, "completed a CPU burst;", (p.b - p.cpu_i), "bursts to go [Q",
                              printNames(readyQ))
                        print(s, "Process", p.n, "switching out of CPU; will block on I/O until time " + str(
                            time + p.io[p.io_i]) + "ms [Q", printNames(readyQ))
                    if (p.cpu_i == (p.b - 1)):  # if(c_counter[plist_RR.index(p)] == p.b):
                        if (time < 1000):
                            print("Process", p.n, "terminated [Q", printNames(readyQ))
                        run_counter = 0
                        plist_SJF.remove(p)
                        running.remove(p)
                    else:
                        running.remove(p)
                        waitingQ.append(p)
            # check if nothing is running
            for p in readyQ:
                if (len(running) == 0):
                    halfswitch = True
                    #do SJF algo
                    running.append(p)
                    readyQ.remove(p)
                    run_counter = 0
                    if (time < 2000):
                        print(s, "Process", p.n, "started using the CPU for " + str(p.cpu[p.cpu_i]) + "ms burst [Q",
                              printNames(readyQ))
            # end of if !switching statement
        # check if any I/O has finished, and if so add to the readyQ. If not, decrement all
        for p in waitingQ:
            if (p.io[p.io_i] == 0):  # if(p.io[0 + i_counter[plist_RR.index(p)]] == 0):
                waitingQ.remove(p)
                p.io_i += 1  # i_counter[plist_RR.index(p)] += 1
                readyQ.append(p)
                if (time < 1000):
                    print(s, "Process", p.n, "completed I/O; added to the ready queue [Q", printNames(readyQ))
            else:
                p.io[p.io_i] -= 1  # p.io[0 + i_counter[plist_RR.index(p)]] -= 1

        # check if any processes arrive
        for p in plist_SJF:
            if (p.a == time):
                # print("CPU times", p.cpu)
                # print("I/O times", p.io)
                readyQ.append(p)
                if (time < 1000):
                    print(s, "Process", p.n, "arrived; added to the ready queue [Q", printNames(readyQ))

        if (switching):
            if (halfswitch):
                target = time + (switchtime / 2)
            else:
                target = time + switchtime
            if (time == target):
                switching = False
                halfswitch = False

        time += 1

        if (len(plist_SJF) == 0):
            break
    print(s, "Simulation ended")
    # end of SJF

if __name__ == "__main__":
    inputlen = len(sys.argv)
    if (not (inputlen == 9 or inputlen == 8)):
        # make the code fucking stop here
        print("bad args")

    numpros = int(sys.argv[1])
    seed = int(sys.argv[2])
    l = float(sys.argv[3])
    expceil = int(sys.argv[4])
    switchtime = int(sys.argv[5])
    alpha = float(sys.argv[6])
    tslice = int(sys.argv[7])
    rradd = "END"  # end
    # check if the optional one is added
    if (inputlen == 9):
        print(sys.argv[8])
        if (sys.argv[8] == "END"):
            rradd = "END"
        elif (sys.argv[8] == "BEGINNING"):
            rradd = "Beginning"
        else:
            print("invalid arg 8")
            print("Testing")

    
    plist_RR = []
    plist_SRT = []
    plist_SJF = []
    plist_FCFS = []

    # fill each list with default processes
    for i in range(numpros):
        plist_SJF.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, math.ceil(1/l), []))
        plist_SRT.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, math.ceil(1/l), []))
        plist_RR.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, math.ceil(1/l), []))
        plist_FCFS.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, math.ceil(1/l), []))

    plist_RR = loadProcesses(plist_RR, seed, l, expceil, alpha)
    plist_SJF = loadProcesses(plist_SJF, seed, l, expceil, alpha)
    plist_SRT = loadProcesses(plist_SRT, seed, l, expceil, alpha)
    plist_FCFS = loadProcesses(plist_FCFS, seed, l, expceil, alpha)

    for p in plist_RR:
        print(p.a,p.b,p.tau)


    
    #SJF(plist_SJF, False, rradd, switchtime)
    roundRobin(plist_FCFS, 999999999, rradd, switchtime)