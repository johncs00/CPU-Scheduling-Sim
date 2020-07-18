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
    def __init__(self, name, cpu_times, io_times, cpu_index, io_index, state, num_burst, arrival_time, turn_time, wait_time, tau_values, tau_index):
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
        self.t = tau_values
        self.t_i = tau_index

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
    
def SJF(listp, tcs, alpha,lambdainput):
    time = 0
    for pid in range(len(listp)):
        print("process", (listp[pid].a))
    #newlist = []
    newlist = sorted(listp, key=lambda x: x.getArrival())
    time += (tcs/2)
    tau = 1/lambdainput
    for pid in range(len(newlist)):
        tau = math.ceil(alpha * burst_io_time[processName][0] + (1 - alpha)) * tau
        print("process2",(newlist[pid].a))
        
def SRT(listp, tcs, alpha, lambdainput):
    time = 0
    target = 0
    halfswitch = False
    switching = False
    for pid in range(len(listp)):
        print("process", (listp[pid].a))
    newlist = []
    newlist = sorted(listp, key=lambda x: x.a)
    tau = 1/lambdainput
    ready_queue = []
    waiting_queue = []
    cpu_copies = []
    for pid in range(len(newlist)):
        #tau = math.ceil(alpha * newlist[pid].getIo() + (1 - alpha) * tau)
        newlist[pid].t.append(tau)
        print("Process", newlist[pid].n,"[NEW] (arrival time", newlist[pid].a, "ms)",newlist[pid].b, "CPU bursts (tau ",
              newlist[pid].t[0], "ms)")
        cpu_copies.append(newlist[pid].cpu[:])
    running = []
    while True:
        s = 'time ' + repr(time) + ':ms'
        if (time == 0):
            print(s, "Simulator started for SRT [Q",printNames(ready_queue))
        if (not switching):
            for pid in running:
                pid.cpu[pid.cpu_i] -= 1
            for pid in range(len(running)):
                if(running[pid].cpu[running[pid].cpu_i] == 0):    #if(p.cpu[0 + c_counter[plist_RR.index(p)]] == 0)
                    swtiching = True        #might only do a halfswitch in readyQ is empty
                    running[pid].cpu_i += 1
                    running[pid].t_i += 1
                           #c_counter[plist_RR.index(p)] += 1
                    if(time < 2000):
                        print(s, "Process", running[pid].n, "(tau ", running[pid].t[running[pid].t_i - 1], "ms) completed a CPU burst;", (running[pid].b - running[pid].cpu_i),"bursts to go [Q",printNames(ready_queue))
                        running[pid].t.append(math.ceil(alpha * cpu_copies[pid][running[pid].cpu_i - 1] + (1 - alpha) * running[pid].t[running[pid].t_i - 1]))
                        print(s, "Recaculated tau =", running[pid].t[running[pid].t_i], "ms for process", running[pid].n, "[Q", printNames(ready_queue))
                        print(s, "Process", running[pid].n, "switching out of CPU; will block on I/O until time " +str(time + running[pid].io[running[pid].io_i])+ "ms [Q", printNames(ready_queue))
                    #print(running[pid].cpu_i)
                    if(running[pid].cpu_i == (running[pid].b - 1)):   #if(c_counter[plist_RR.index(p)] == p.b):
                        if(time < 1000):
                            print("Process", running[pid].n, "(tau ", running[pid].t[running[pid].t_i], "ms) terminated [Q", printNames(ready_queue))
                        newlist.remove(running[pid])
                        running.remove(running[pid])
                    else:
                        waiting_queue.append(running.pop(pid))                
            for pid in ready_queue:
                if(len(running) == 0):
                    halfswtich = True
                    running.append(pid)
                    ready_queue.remove(pid)
                    run_counter = 0
                    if(time < 2000):
                        print(s, "Process", pid.n, "(tau ", pid.t[pid.t_i], "ms) started using the CPU for " + str(pid.cpu[pid.cpu_i]) +  "ms burst [Q",printNames(ready_queue))
        for pid in waiting_queue:
            if(pid.io[pid.io_i] == 0): 
                waiting_queue.remove(pid)
                pid.io_i += 1
                if (len(running) > 0):
                    if (pid.cpu[pid.cpu_i] < (running[0].cpu[running[0].cpu_i])):
                        ready_queue.append(running[0])
                        if(time < 1000):
                            print(s, "Process", pid.n, "(tau ", pid.t[pid.t_i], "ms) completed I/O; preempting", running[0], " [Q", printNames(ready_queue))                    
                        running.remove(running[0])
                        running.append(pid)
                    else:
                        ready_queue.append(pid)
                        if(time < 1000):
                            print(s, "Process", pid.n, "(tau ", pid.t[pid.t_i], "ms) completed I/O; added to the ready queue [Q", printNames(ready_queue))                
                else:
                    ready_queue.append(pid)
                    if(time < 1000):
                        print(s, "Process", pid.n, "(tau ", pid.t[pid.t_i], "ms) completed I/O; added to the ready queue [Q", printNames(ready_queue))
            else:
                pid.io[pid.io_i] -= 1
        for pid in newlist:
            if (time == pid.a):
                '''pid.getArrival()'''
                ready_queue.append(pid)
                if(time < 1000):
                    print(s, "Process", pid.n, "(tau ", pid.t[pid.t_i], "ms) arrived; added to the ready queue [Q",printNames(ready_queue))                 
                
        '''if (len(ready_queue) > 0):
            ready_queue.sort(key=lambda x: x.getCpu())
            if (running == None):
                running = ready_queue.pop(0)
            elif (ready_queue[0].getCpu() < (running.getCpu())):
                ready_queue.append(running)
                running = ready_queue.pop(0)'''
        
        #print(count)
        if(switching):
            if(halfswtich):
                target = time + (tcs/2)
            else:
                target = time + tcs
            if(time == target):
                swithcing = False
                halfswtich = False        
        time += 1   
        if (len(newlist) <= 0):
            break
            
        
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

    numpros = 2 #int(sys.argv[1])
    seed = 2 #int(sys.argv[2])
    l = 0.01 #float(sys.argv[3])
    expceil = 256 #int(sys.argv[4])
    switchtime = 4 #int(sys.argv[5])
    alpha = 0.5 #float(sys.argv[6])
    tslice = 128 #int(sys.argv[7])
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
        plist_RR.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, 0, [], 0))   #Adds process into the list, all times set to 0 and default state of 1
        plist_SJF.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, 0, [], 0))
        plist_SRT.append(Process(process_names[i], [], [], 0, 0, 0, 0, 0, 0, 0, [], 0))
        plist_FCFS.append(Process(process_names[i], [], [], 1, 0, 0, 0, 0, 0, 0, [], 0))
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
    SRT(plist_SRT, switchtime, alpha, l)