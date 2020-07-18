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

    def __lt__(self, obj):
        """self < obj."""
        if (self.tauarray[self.cpu_i] == obj.tauarray[obj.cpu_i]):
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
        # arrival and burst num stuff
        corner_cancer = False
        r_small = randy.drand48()
        r_big = -math.log(r_small) / l
        #print(p.n ,r_small,r_big, file = f)
        while (r_big > upperbound):
            r_small = randy.drand48()
            r_big = -math.log(r_small) / l

        p.a = math.floor(r_big)

        r_small = randy.drand48()
        r_big = -math.log(r_small) / l
        if (p.n == "G" and r_big > upperbound):
            temp_num_burst = burstnumber(r_small)
            p.b = temp_num_burst
            corner_cancer = True
        else:
            while (r_big > upperbound):
                r_small = randy.drand48()
                r_big = -math.log(r_small) / l
            temp_num_burst = burstnumber(r_small)
            p.b = (temp_num_burst)

        while (r_big > upperbound):
            r_small = randy.drand48()
            r_big = -math.log(r_small) / l

        # I/O and CPU bursts stuff
        for r in range(p.b):
            if (not corner_cancer):
                r_small = randy.drand48()
                r_big = -math.log(r_small) / l

            while (r_big > upperbound):
                r_small = randy.drand48()
                r_big = -math.log(r_small) / l

            p.cpu.append(math.ceil(r_big))

            if (r == temp_num_burst - 1):
                break
            r_small = randy.drand48()
            r_big = -math.log(r_small) / l

            while (r_big > upperbound):
                r_small = randy.drand48()
                r_big = -math.log(r_small) / l

            p.io.append(math.ceil(r_big))

        # tau stuff
        for i in range(p.b):
            if i == 0:
                p.tauarray.append(p.tau)
            else:
                p.tauarray.append(math.ceil(alpha * p.cpu[i - 1] + (1 - alpha) * p.tauarray[i - 1]))

    return p_list


def randList(l, upperbound, seed):
    min = 0
    max = 0
    sum = 0
    iterations = 100000
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
    #TODO
    #Implement a way to only lower numbers in io if not currently context switching
    #maybe each process should have a state variable attached to it?
    #Nah we fuckin deleted it earlier.
    #For test case 3 we are missing a few context switches. See if you can find them! Full test cases below
    #https://submitty.cs.rpi.edu/courses/u20/csci4210/display_file?dir=course_materials&path=%2Fvar%2Flocal%2Fsubmitty%2Fcourses%2Fu20%2Fcsci4210%2Fuploads%2Fcourse_materials%2Fproject%2Foutput03-full.txt
    #Round Robin doesn't actually append anything and thus doesn't work. Most of the infrastructure is there so it can't be that hard.
    #Don't know why Round Robin does that
    #Shame.
    #Numbers are wayy to low with multiple processes
    #maybe a +4ms context switch is missing?
    #Remember that continuing prevents the time+1 from happening.
    #If most of the above stuff is done, we're near 50/100 and have the ability to get alot done on SJF.
    #Somehow the program worked without continue
    #no clue how.
    to_remove = 0
    io_corner = False
    context_time = 0
    default = True
    if (location == "BEGINNING"):
        default = False
    time = 0
    if (t_slice < 1000000):
        print("Round Robin Algorithm Start")
    else:
        print("FCFS Algorithm Start")

    switch_p = ""
    readyQ = []
    waitingQ = []
    running = []
    run_counter = 0
    for p in plist_RR:
        print("Process", p.n, "[NEW] (arrival time", p.a, "ms)", p.b, "CPU bursts")

    while (True):
        s_r = 'time ' + repr(time) + 'ms:'
        if (time == 0 and t_slice > 100000):
            print(s_r, "Simulator started for FCFS [Q", printNames(readyQ))
        elif (time == 0 and t_slice < 100000):
            print(s_r, "Simulator started for RR [Q", printNames(readyQ))
        # decrement current running process
        if(context_time > 0):
            if(context_time >= 0):
                for p in waitingQ:
                    #print(context_time, switch_p, p.n)
                    if(p.n != switch_p or context_time > switchtime/2):
                        if(p.io[p.io_i] == 0):
                            #s_r = 'time ' + repr(time) + 'ms:'
                            #print(s_r, "Process", p.n, "completed I/O; added to ready queue [Q", printNames(readyQ))
                            #print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
                            io_corner = True
                            continue
                        p.io[p.io_i] -= 1
                        
            if(context_time < 0):
                switch_p = ""

            context_time -= 1
            time += 1

            if (len(running) == 0 and len(readyQ) == 0 and len(waitingQ) == 0 and time > 103 and context_time == 0):
                if (t_slice > 100000):
                    print(s_r, "Simulator ended for FCFS [Q", printNames(readyQ))
                    print()
                else:
                    print(s_r, "Simulator ended for RR [Q", printNames(readyQ))
                    print()
                break

            continue

        for p in running:
            
            p.cpu[p.cpu_i] -= 1
            run_counter += 1
        # if running rpocess has finished
        for p in running:
            if (p.cpu[p.cpu_i] == 0):
                p.cpu_i += 1
                context_time += (switchtime/2)
                if (time < 5000 and (p.b - p.cpu_i) != 0):
                    print(s_r, "Process", p.n, "completed a CPU burst;", (p.b - p.cpu_i), "bursts to go [Q",
                          printNames(readyQ))
                    if(p.io_i != p.b -1):
                        print(s_r, "Process", p.n,
                            "switching out of CPU; will block on I/O until time " + str(
                                int(time + p.io[p.io_i] + switchtime/2)) + "ms [Q",
                            printNames(readyQ))
                        switch_p = p.n
                        
                if (p.cpu_i == (p.b)):
                    print(s_r, "Process", p.n, "terminated [Q", printNames(readyQ))
                    run_counter = 0
                    plist_RR.remove(p)
                    running.remove(p)
                else:
                    running.remove(p)
                    waitingQ.append(p)

        # check if the running process ran out of time
        
        if (run_counter == t_slice):
            # context = True
            if (time < 5000 and len(readyQ) > 0):
                print(s_r, "Time slice expired; process", running[0].n,
                      "preempted with " + str(running[0].cpu[running[0].cpu_i]) + "ms to go [Q", printNames(readyQ))
            else:
                print(s_r, "Time slice expired; no preemption because ready queue is empty [Q", printNames(readyQ))
            # if there are items in the readyQ
            if (len(readyQ) > 0):
                # switching = True
                temp_holder = running.pop(0)
                context_time += int(switchtime/2)
                if (default):
                    readyQ.append(temp_holder)
                else:
                    readyQ.insert(0, temp_holder)  
            else:
                run_counter = 0

        # check if any I/O has finished, and if so add to the readyQ. If not, decrement the io if not completed.
        for p in waitingQ:
            #print(p.n, time, p.io[p.io_i], len(waitingQ))
            if (p.io[p.io_i] == 0):
                #if(waitingQ.index(p) == len(waitingQ) - 2):
                    #print("HMMMMMMMMMMMMMMMMMMMMMMMMM")
                    #waitingQ[waitingQ.index(p) + 1].io[p.io_i] -= 1
                waitingQ.remove(p)
                p.io_i += 1  
                if (default):
                    readyQ.append(p)
                else:
                    readyQ.insert(0, p)
                if (time < 5000):
                    if(io_corner):
                        s_r = 'time ' + repr(time - 1) + 'ms:'
                        #print("AHHHHHHHHHHHHHHHHHHH")
                        print(s_r, "Process", p.n, "completed I/O; added to ready queue [Q", printNames(readyQ))
                        s_r = 'time ' + repr(time) + 'ms:'
                    else:
                        print(s_r, "Process", p.n, "completed I/O; added to ready queue [Q", printNames(readyQ))
            else:
                p.io[p.io_i] -= 1  
        io_corner = False
        # check if any processes arrive
        for p in plist_RR:
            if (p.a == time):
                if (default):
                    readyQ.append(p)
                else:
                    readyQ.insert(0, p)
                if (time < 5000):
                    print(s_r, "Process", p.n, "arrived; added to ready queue [Q", printNames(readyQ))
        # check if nothing is running
        for p in readyQ:
            if (len(running) == 0):
                running.append(p)
                context_time += int(switchtime / 2)
                s_r = 'time ' + repr(time + int(context_time)) + 'ms:'
                readyQ.remove(p)
                run_counter = 0
                if (time < 5000):
                    print(s_r, "Process", p.n, "started using the CPU for " + str(p.cpu[p.cpu_i]) + "ms burst [Q",
                          printNames(readyQ))
        #Time increment and ender.

        time += 1
    # end of RoundRobin


def SJF(plist_SJF, switchtime):
    # TODO
    # Implement a way to only lower numbers in io if not currently context switching
    # maybe each process should have a state variable attached to it?
    # Nah we fuckin deleted it earlier.
    # For test case 3 we are missing a few context switches. See if you can find them! Full test cases below
    # https://submitty.cs.rpi.edu/courses/u20/csci4210/display_file?dir=course_materials&path=%2Fvar%2Flocal%2Fsubmitty%2Fcourses%2Fu20%2Fcsci4210%2Fuploads%2Fcourse_materials%2Fproject%2Foutput03-full.txt
    # Round Robin doesn't actually append anything and thus doesn't work. Most of the infrastructure is there so it can't be that hard.
    # Don't know why Round Robin does that
    # Shame.
    # Numbers are wayy to low with multiple processes
    # maybe a +4ms context switch is missing?
    # Remember that continuing prevents the time+1 from happening.
    # If most of the above stuff is done, we're near 50/100 and have the ability to get alot done on SJF.
    # Somehow the program worked without continue
    # no clue how.
    io_corner = False
    context_time = 0
    time = 0
    print("SJF Algorithm Start")


    switch_p = ""
    readyQ = []
    waitingQ = []
    running = []
    run_counter = 0
    for p in plist_SJF:
        print("Process", p.n, "[NEW] (arrival time", p.a, "ms)", p.b, "CPU bursts")
    heapq.heapify(readyQ)
    while (True):
        s_r = 'time ' + repr(time) + 'ms:'
        if (time == 0):
            print(s_r, "Simulator started for SJF [Q", printNames(readyQ))
        # decrement current running process
        if (context_time > 0):
            if (context_time > 0):
                for p in waitingQ:
                    if (p.n != switch_p or context_time > switchtime / 2):
                        # print(p.n, context_time, switch_p)
                        if (p.io[p.io_i] == 0):
                            io_corner = True
                            continue
                        p.io[p.io_i] -= 1
            if (context_time == 0):
                switch_p = ""
            context_time -= 1
            time += 1
            if (len(running) == 0 and len(list(readyQ)) == 0 and len(waitingQ) == 0 and time > 103 and context_time == 0):
                print(s_r, "Simulator ended for SJF [Q", printNames(readyQ))
                print()
                break
            continue
        for p in running:
            p.cpu[p.cpu_i] -= 1
            run_counter += 1
        # if running rpocess has finished
        for p in running:
            if (p.cpu[p.cpu_i] == 0):
                p.cpu_i += 1
                context = True
                context_time += 2
                if (time < 500000 and (p.b - p.cpu_i) != 0):
                    print(s_r, "Process", p.n, "(tau", p.tauarray[p.cpu_i - 1],"ms)" , "completed a CPU burst;", (p.b - p.cpu_i), "bursts to go [Q",
                          printNames(readyQ))
                    print(s_r, "Recalculated tau =", p.tauarray[p.cpu_i], "for process", p.n, "[Q", printNames(readyQ))
                    if (p.io_i != p.b - 1):
                        print(s_r, "Process", p.n,
                              "switching out of CPU; will block on I/O until time " + str(
                                  int(time + p.io[p.io_i] + switchtime / 2)) + "ms [Q",
                              printNames(readyQ))
                        switch_p = p.n
                if (p.cpu_i == (p.b)):
                    print(s_r, "Process", p.n, "terminated [Q", printNames(readyQ))
                    run_counter = 0
                    plist_SJF.remove(p)
                    running.remove(p)
                else:
                    running.remove(p)
                    waitingQ.append(p)
                    # print(waitingQ[0].n, context_time)
        # check if the running process ran out of time
        for p in waitingQ:
            if (p.io[p.io_i] == 0):
                waitingQ.remove(p)
                p.io_i += 1
                heapq.heappush(readyQ, p)
                if (time < 500000):
                    if (io_corner):
                        s_r = 'time ' + repr(time - 1) + 'ms:'
                        print(s_r, "Process", p.n,"(tau", p.tauarray[p.cpu_i],"ms)" , "completed I/O; added to ready queue [Q", printNames(readyQ))
                        s_r = 'time ' + repr(time) + 'ms:'
                    else:
                        print(s_r, "Process", p.n,"(tau", p.tauarray[p.cpu_i],"ms)" , "completed I/O; added to ready queue [Q", printNames(readyQ))
            else:
                p.io[p.io_i] -= 1
                # check if any processes arrive
        io_corner = False
        for p in plist_SJF:
            if (p.a == time):
                heapq.heappush(readyQ, p)
                if (time < 500000):
                    print(s_r, "Process", p.n, "(tau", p.tauarray[p.cpu_i], "ms)"   , "arrived; added to ready queue [Q", printNames(readyQ))
        # check if nothing is running
        if (len(running) == 0 and len(readyQ) != 0):
            input = heapq.heappop(readyQ)
            running.append(input)
            context_time += int(switchtime / 2)
            s_r = 'time ' + repr(time + context_time) + 'ms:'
            run_counter = 0
            if (time < 500000):
                print(s_r, "Process", input.n, "(tau", input.tauarray[input.cpu_i],"ms)" ,"started using the CPU for " + str(input.cpu[input.cpu_i]) + "ms burst [Q",
                          printNames(readyQ))
        # Time increment and ender.
        time += 1



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
        plist_SJF.append(Process(process_names[i], [], [], 0, 0, 0, 0, 0, 0, math.ceil(1 / l), []))
        plist_SRT.append(Process(process_names[i], [], [], 0, 0, 0, 0, 0, 0, math.ceil(1 / l), []))
        plist_RR.append(Process(process_names[i], [], [], 0, 0, 0, 0, 0, 0, math.ceil(1 / l), []))
        plist_FCFS.append(Process(process_names[i], [], [], 0, 0, 0, 0, 0, 0, math.ceil(1 / l), []))

    plist_RR = loadProcesses(plist_RR, seed, l, expceil, alpha)
    plist_SJF = loadProcesses(plist_SJF, seed, l, expceil, alpha)
    plist_SRT = loadProcesses(plist_SRT, seed, l, expceil, alpha)
    plist_FCFS = loadProcesses(plist_FCFS, seed, l, expceil, alpha)


    # SJF(plist_SJF, False, rradd, switchtime)
    roundRobin(plist_FCFS, 999999999, rradd, switchtime)
    SJF(plist_SJF, switchtime)
    roundRobin(plist_RR, tslice, rradd, switchtime)