import sys
import time
import random as rand
import math


r_list = []
x_list = []
process_names = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

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
        self.cpu_i = cpu_index  #Starts at zero, index for the list of cpu burst times. keep track of it
        self.io_i = io_index    #Starts at zero, index for the list of I/O burst times. keep track of it
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

def loadProcesses(p_list, numpros, seed, l, upperbound):
    

def randList(l, upperbound, seed):
    min = 0
    max = 0
    sum = 0
    iterations = 100000
    #l = 0.001  
    ans = []
    randy = rand(seed)
    randy.srand48(seed)
    for i in range(iterations):
        #replace random() with drand48
        r = randy.drand48()   #/ * uniform # dist[0.00, 1.00) -- also check out random() * /
        x = -math.log(r) / l   # / lambda; / * log() is natural log * /
        # / * avoid values that are far down the "long tail" of the distribution * /
        r_list.append(r)
        #yield (x,r)
        if (x > upperbound):
            i -= 1
            continue
            #print("x is ", x)
        pair = (x, r)
        ans.append(pair)
        sum += x
        if (i == 0 or x < min):
            min = x
        if ( i == 0 or x > max ):
            max = x
        
        avg = sum / iterations

    return ans

    #print( "minimum value: ", min)
    #print( "maximum value: ", max)
    #print( "average value: ", avg)


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
        print("Process", p.n,"[NEW] (arrival time", p.a, "ms)",p.b, "CPU bursts")

    while(True):
        #time string
        #real time
        s_r = 'time ' + repr(time) + 'ms:'
        #context adjusted time
        s_c = 'time ' + repr(time + context_time) + 'ms:'
        if(time == 0 and t_slice > 100000):
            print(s_r, "Simulator started for FCFS [Q",printNames(readyQ))
        elif(time == 0 and t_slice < 100000):
            print(s_r, "Simulator started for RR [Q",printNames(readyQ))


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

        #context switch
        if(not context): #------ Print the process when we find it, using time + context_time, then suspend ops intil the printed time.

            #decrement the running process, does nothing if there is no running process
       

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


            for p in running:
                #p.cpu[0 + c_counter[plist_RR.index(p)]] -= 1
                p.cpu[p.cpu_i] -= 1
                run_counter += 1

            #end of if context switch statement

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

        
        '''
        if(switching):
            if(halfswtich):
                target = time + (switchtime/2)
            else:
                target = time + switchtime
            if(time == target):
                swithcing = False
                halfswtich = False
        '''
        '''
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
    
    
    plist_RR = []
    plist_SRT = []
    plist_SJF = []
    plist_FCFS = []

    for i in range(numpros):
        plist_RR.append(Process(process_names[i], [], [], 0, 0, 0, 0, 0, 0, 0))   #Adds process into the list, all times set to 0 and default state of 1
        plist_SJF.append(Process(process_names[i], [], [], 0, 0, 0, 0, 0, 0, 0))
        plist_SRT.append(Process(process_names[i], [], [], 0, 0, 0, 0, 0, 0, 0))
        plist_FCFS.append(Process(process_names[i], [], [], 0, 0, 0, 0, 0, 0, 0))
    
    #fill each list with default processes
    
    #DO calculations to give proceses their rime values.

    interarrival = randList(l, expceil, seed)
    print(len(r_list), len(interarrival))
    rand_index = 0
    r_index = 0

    '''
    for p in plist_RR:
        p.a = (math.floor(interarrival[rand_index][0]))
        #p.a = (math.floor(x_list[rand_index]))
        
        rand_index +=1
        r_index +=1
        while(r_list[r_index] < 0.01):
            r_index +=1

        if(interarrival[rand_index][1] != r_list[r_index]):
            temp_num_burst = burstnumber(r_list[r_index])
            r_index +=1
        else:
            temp_num_burst = burstnumber(interarrival[rand_index][1])
            rand_index +=1
            r_index +=1
            while(r_list[r_index] < 0.01):
                r_index +=1

        p.b = int(temp_num_burst)
        for r in range(temp_num_burst):
            p.cpu.append(math.ceil(interarrival[rand_index][0]))
            #p.cpu.append(math.ceil(x_list[rand_index]))
            rand_index +=1
            r_index +=1
            while(r_list[r_index] < 0.01):
                r_index +=1
            if(r == temp_num_burst - 1):
                break
            p.io.append(math.ceil(interarrival[rand_index][0]))
            #p.io.append(math.ceil(x_list[rand_index]))
            rand_index +=1
            r_index +=1
            while(r_list[r_index] < 0.01):
                r_index +=1

    rand_index = 0
    

    rand_index = 0
    for p in plist_SJF:
        #p.a = (math.floor(interarrival[rand_index][0]))
        p.a = (math.floor(x_list[rand_index]))
        rand_index +=1
        #temp_num_burst = burstnumber(interarrival[rand_index][1])
        temp_num_burst = burstnumber(r_list[rand_index])
        p.b = (temp_num_burst)
        rand_index +=1
        for r in range(temp_num_burst):
            #p.cpu.append(math.ceil(interarrival[rand_index][0]))
            p.cpu.append(math.ceil(x_list[rand_index]))
            rand_index +=1
            if(r == temp_num_burst - 1):
                break
            #p.io.append(math.ceil(interarrival[rand_index][0]))
            p.io.append(math.ceil(x_list[rand_index]))
            rand_index +=1

    rand_index = 0
    for p in plist_FCFS:
        #p.a = (math.floor(interarrival[rand_index][0]))
        p.a = (math.floor(x_list[rand_index]))
        rand_index +=1
        #temp_num_burst = burstnumber(interarrival[rand_index][1])
        temp_num_burst = burstnumber(r_list[rand_index])
        p.b = int(temp_num_burst)
        rand_index +=1
        for r in range(temp_num_burst):
            #p.cpu.append(math.ceil(interarrival[rand_index][0]))
            p.cpu.append(math.ceil(x_list[rand_index]))
            rand_index +=1
            if(r == temp_num_burst - 1):
                break
            #p.io.append(math.ceil(interarrival[rand_index][0]))
            p.io.append(math.ceil(x_list[rand_index]))
            rand_index +=1
    '''


    #first one is FCFS, hence the giant timeslice
    #roundRobin(plist_FCFS, 999999999, rradd, switchtime)
    roundRobin(plist_RR, tslice, rradd, switchtime)
    

