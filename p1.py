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
    def __init__(self, name, cpu_times, io_times, cpu_index, io_index, state, num_burst, arrival_time, turn_time, wait_time):
        self.n = name
        self.cpu = cpu_times
        self.io = io_times
        self.cpu_i = cpu_index
        self.io_i = io_index
        self.s = state
        self.b = num_burst
        self.a = arrival_time
        self.turn = turn_time
        self.wait = wait_time

def burstnumber(input):
    input = input * 100
    input = math.trunc(input)
    input += 1
    return input

def printNames(ready_queue):
    if(len(ready_queue) == 0):
        return "<empty>]"
    string = ""
    for p in ready_queue:
        if(ready_queue.index(p) == (len(ready_queue) - 1)):
            string += p.n + "]"
        else:
            string += p.n + " "
    return string

def randList(l, upperbound, seed):
    min = 0
    max = 0
    sum = 0
    iterations = 100000
    #l = 0.001  
    r_list = []
    randy = rand(seed)
    randy.srand48(seed)
    for i in range(iterations):
        #replace random() with drand48
        r = randy.drand48()   #/ * uniform # dist[0.00, 1.00) -- also check out random() * /
        x = -math.log(r) / l   # / lambda; / * log() is natural log * /
        # / * avoid values that are far down the "long tail" of the distribution * /
        if (x > upperbound):
            i -= 1
            continue
            #print("x is ", x)
        pair = (x,r)
        r_list.append(pair)
        sum += x
        if (i == 0 or x < min):
            min = x
        if ( i == 0 or x > max ):
            max = x
        
        avg = sum / iterations

    return r_list
    #print( "minimum value: ", min)
    #print( "maximum value: ", max)
    #print( "average value: ", avg)


def roundRobin(plist_RR, t_slice, location, switchtime):
    #plist_RR -- list of processes
    #t_slice -- alloted time for CPU bursts 
    #location -- "Beginning" or "End", determines where process are pushed into the queue
    switching = False
    halfswtich = False
    
    default = True
    if(location == "BEGINNING"):
        default = False
        '''
    #keeps track of the number of cpu-bursts a process has completed
    c_counter = []
    for i in range(len(plist_RR)):
        c_counter.append(0)
    #keeps track of the number of I/0-bursts a process has completed
    i_counter = []
    for i in range(len(plist_RR)):
        i_counter.append(0)
        '''

    time = 0
    target = 0
    '''
    if(t_slice < 1000000):
        print("Round Robin Algorithm Start")
    else:
        print("FCFS Algorithm Start")
    '''
    readyQ = []
    waitingQ = []
    running = []
    run_counter = 0

    for p in plist_RR:
        print("Process", p.n,"[NEW] (arrival time", p.a, "ms) ",p.b, "CPU bursts")

    while(True):
        #time string
        s = 'time ' + repr(time) + ':ms'
        if(time == 0 and t_slice > 100000):
            print(s, "Simulator started for FCFS [Q",printNames(readyQ))
        elif(time == 0 and t_slice < 100000):
            print(s, "Simulator started for RR [Q",printNames(readyQ))
        #context switch
        if(not switching):
            #decrement the running process, does nothing if there is no running process
            for p in running:
                #p.cpu[0 + c_counter[plist_RR.index(p)]] -= 1
                p.cpu[p.cpu_i] -= 1
                run_counter += 1
                    

            #check if the running process finished
            for p in running:
                if(p.cpu[p.cpu_i] == 0):    #if(p.cpu[0 + c_counter[plist_RR.index(p)]] == 0)
                    swtiching = True        #might only do a halfswitch in readyQ is empty
                    p.cpu_i += 1
                           #c_counter[plist_RR.index(p)] += 1
                    if(time < 2000):
                        print(s, "Process", p.n, "completed a CPU burst;", (p.b - p.cpu_i),"bursts to go [Q",printNames(readyQ))
                        print(s, "Process", p.n, "switching out of CPU; will block on I/O until time " +str(time + p.io[p.io_i])+ "ms [Q", printNames(readyQ))
                    if(p.cpu_i == (p.b - 1)):   #if(c_counter[plist_RR.index(p)] == p.b):
                        if(time < 1000):
                            print("Process", p.n, "terminated [Q", printNames(readyQ))
                        run_counter = 0
                        plist_RR.remove(p)
                        running.remove(p)
                    else:
                        running.remove(p)
                        waitingQ.append(p)

            #check if the running process ran out of time
            if(run_counter == t_slice):
                if(time < 1000):
                    print(s, "Time slice expired; process", running[0].n, "preempted with " + str(running[0].cpu[running[0].cpu_i]) + "ms to go [Q",printNames(readyQ))
                #if there are items in the readyQ
                if(len(readyQ) > 0):
                    swithcing = True
                    temp_holder = running.pop(0)
                    if(default):
                        readyQ.append(temp_holder)
                    else:
                        readyQ.insert(0, temp_holder)
                else:
                    #Check this line for errors
                    run_counter = 0

            #check if nothing is running
            for p in readyQ:
                if(len(running) == 0):
                    halfswtich = True
                    running.append(p)
                    readyQ.remove(p)
                    run_counter = 0
                    if(time < 2000):
                        print(s, "Process", p.n, "started using the CPU for " + str(p.cpu[p.cpu_i]) +  "ms burst [Q",printNames(readyQ))
            #end of if !switching statement

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
                    print(s, "Process", p.n, "completed I/O; added to the ready queue [Q", printNames(readyQ))
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
                    print(s, "Process", p.n, "arrived; added to the ready queue [Q",printNames(readyQ))

        if(switching):
            if(halfswtich):
                target = time + (switchtime/2)
            else:
                target = time + switchtime
            if(time == target):
                swithcing = False
                halfswtich = False

        time += 1

        if(len(plist_RR) == 0):
            break
    #end of RoundRobin
    
if __name__ == "__main__":
    inputlen = len(sys.argv)
    if (not(inputlen == 9 or inputlen == 8)):
        #make the code fucking stop here
        print("bad args")

    numpros = int(sys.argv[1])
    seed = int(sys.argv[2])
    l = float(sys.argv[3])
    expceil = int(sys.argv[4])
    switchtime = int(sys.argv[5])
    alpha = float(sys.argv[6])
    tslice = int(sys.argv[7])
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
            #r = rand.random()
            print(r)        
            
    #bursttest = 0.0856756876765
    #bursttest = burstnumber(bursttest)
    #print(bursttest, "This should be 9")
    
    #replace l with argv[3]
    #replace upperbound with argv[4]
    
    process_names = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    plist_RR = []
    plist_SRT = []
    plist_SJF = []
    plist_FCFS = []
    
    #fill each list with default processes
    for i in range(numpros):
        plist_RR.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, 0))   #Adds process into the list, all times set to 0 and default state of 1
        plist_SJF.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, 0))
        plist_SRT.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, 0))
        plist_FCFS.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, 0))
    #DO calculations to give proceses their rime values.

    interarrival = randList(l, expceil, seed)

    rand_index = 0;
    for p in plist_RR:
        p.a = (math.floor(interarrival[rand_index][0]))
        rand_index +=1
        temp_num_burst = burstnumber(interarrival[rand_index][1])
        p.b = (temp_num_burst)
        rand_index +=1
        for r in range(temp_num_burst):
            p.cpu.append(math.ceil(interarrival[rand_index][0]))
            rand_index +=1
            if(r == temp_num_burst - 1):
                break
            p.io.append(math.ceil(interarrival[rand_index][0]))
            rand_index +=1

    rand_index = 0
    for p in plist_SRT:
        p.a = (math.floor(interarrival[rand_index][0]))
        rand_index +=1
        temp_num_burst = burstnumber(interarrival[rand_index][1])
        p.b = (temp_num_burst)
        rand_index +=1
        for r in range(temp_num_burst):
            p.cpu.append(math.ceil(interarrival[rand_index][0]))
            rand_index +=1
            if(r == temp_num_burst - 1):
                break
            p.io.append(math.ceil(interarrival[rand_index][0]))
            rand_index +=1

    rand_index = 0
    for p in plist_SJF:
        p.a = (math.floor(interarrival[rand_index][0]))
        rand_index +=1
        temp_num_burst = burstnumber(interarrival[rand_index][1])
        p.b = (temp_num_burst)
        rand_index +=1
        for r in range(temp_num_burst):
            p.cpu.append(math.ceil(interarrival[rand_index][0]))
            rand_index +=1
            if(r == temp_num_burst - 1):
                break
            p.io.append(math.ceil(interarrival[rand_index][0]))
            rand_index +=1

    rand_index = 0
    for p in plist_FCFS:
        p.a = (math.floor(interarrival[rand_index][0]))
        rand_index +=1
        temp_num_burst = burstnumber(interarrival[rand_index][1])
        p.b = (temp_num_burst)
        rand_index +=1
        for r in range(temp_num_burst):
            p.cpu.append(math.ceil(interarrival[rand_index][0]))
            rand_index +=1
            if(r == temp_num_burst - 1):
                break
            p.io.append(math.ceil(interarrival[rand_index][0]))
            rand_index +=1


    #for p in plist_RR:
        #print(p.b)

    #first one is FCFS, hence the giant timeslice
    roundRobin(plist_FCFS, 999999999, rradd, switchtime)
    roundRobin(plist_RR, tslice, rradd, switchtime)
    

