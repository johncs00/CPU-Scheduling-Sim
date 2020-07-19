def SRT(plist_SRT, switchtime):
    io_corner = False
    context_time = 0
    time = 0
    print("SRT Algorithm Start")
    switch_p = ""
    readyQ = []
    waitingQ = []
    running = []
    run_counter = 0
    for p in plist_SRT:
        print("Process", p.n, "[NEW] (arrival time", p.a, "ms)", p.b, "CPU bursts")
    heapq.heapify(readyQ)
    while (True):
        #print(time)
        preempted = False
        s_r = 'time ' + repr(time) + 'ms:'
        if (time == 0):
            print(s_r, "Simulator started for SRT [Q", printNames(readyQ))
        # decrement current running process
        if (context_time > 0):
            if (context_time > 0):
                #print(context_time, time, switch_p)   
                for p in waitingQ:
                    #print(switch_p)
                    #switch_p = ""
                    if (p.n != switch_p or context_time > switchtime / 2):
                        # print(p.n, context_time, switch_p)
                        if (p.io[p.io_i] == 0):
                            io_corner = True
                            continue
                        p.io[p.io_i] -= 1       
            context_time -= 1
            if (context_time == 0):
                switch_p = ""
            time += 1
            #print(time)
            if (len(running) == 0 and len(list(readyQ)) == 0 and len(
                    waitingQ) == 0 and time > 103 and context_time == 0):
                print(s_r, "Simulator ended for SRT [Q", printNames(readyQ))
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
                if (time < 1000 and (p.b - p.cpu_i) != 0):
                    print(s_r, "Process", p.n, "(tau", p.tauarray[p.cpu_i - 1], "ms)", "completed a CPU burst;",
                          (p.b - p.cpu_i), "bursts to go [Q",
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
        #print(time)
        for p in waitingQ:
            #print(p.n, p.io[p.io_i], time)
            if (p.io[p.io_i] == 0):
                waitingQ.remove(p)
                p.io_i += 1
                if (len(running) > 0):
                    if (p.tauarray[p.cpu_i] < running[0].tauarray[running[0].cpu_i]):
                        if (time < 1000):
                            if (io_corner):
                                s_r = 'time ' + repr(time - 1) + 'ms:'
                                print(s_r, "Process", p.n, "(tau", p.tauarray[p.cpu_i], "ms)",
                                      "completed I/O; preempting", running[0].n, "[Q", printNames(readyQ))
                                s_r = 'time ' + repr(time) + 'ms:'
                            else:
                                print(s_r, "Process", p.n, "(tau", p.tauarray[p.cpu_i], "ms)",
                                      "completed I/O; preempting", running[0].n, "[Q", printNames(readyQ))
                        heapq.heappush(readyQ, running.pop(0))
                        running.append(p)                       
                        preempted = True
                        
                    else:
                        heapq.heappush(readyQ, p)
                        if (time < 1000):
                            if (io_corner):
                                s_r = 'time ' + repr(time - 1) + 'ms:'
                                print(s_r, "Process", p.n, "(tau", p.tauarray[p.cpu_i], "ms)",
                                      "completed I/O; added to ready queue [Q", printNames(readyQ))
                                s_r = 'time ' + repr(time) + 'ms:'
                            else:
                                print(s_r, "Process", p.n, "(tau", p.tauarray[p.cpu_i], "ms)",
                                      "completed I/O; added to ready queue [Q", printNames(readyQ))
                else:
                    heapq.heappush(readyQ, p)
                    if (time < 1000):
                        if (io_corner):
                            s_r = 'time ' + repr(time - 1) + 'ms:'
                            print(s_r, "Process", p.n, "(tau", p.tauarray[p.cpu_i], "ms)",
                                  "completed I/O; added to ready queue [Q", printNames(readyQ))
                            s_r = 'time ' + repr(time) + 'ms:'
                        else:
                            print(s_r, "Process", p.n, "(tau", p.tauarray[p.cpu_i], "ms)",
                                  "completed I/O; added to ready queue [Q", printNames(readyQ))
            else:
                p.io[p.io_i] -= 1
                # check if any processes arrive
        io_corner = False
        for p in plist_SRT:
            if (p.a == time):
                heapq.heappush(readyQ, p)
                if (time < 1000):
                    print(s_r, "Process", p.n, "(tau", p.tauarray[p.cpu_i], "ms)", "arrived; added to ready queue [Q",
                          printNames(readyQ))
        # check if nothing is running
        #print(len(readyQ))
        if (not preempted and len(running) == 0 and len(readyQ) != 0):
            input = heapq.heappop(readyQ)
            running.append(input)
            context_time += int(switchtime / 2)
            s_r = 'time ' + repr(time + context_time) + 'ms:'
            run_counter = 0
            if (time < 1000):
                print(s_r, "Process", running[0].n, "(tau", running[0].tauarray[running[0].cpu_i], "ms)",
                      "started using the CPU for " + str(running[0].cpu[running[0].cpu_i]) + "ms burst [Q",
                      printNames(readyQ))
        if (preempted and len(running) == 1 and len(readyQ) != 0):
            context_time += int(switchtime)
            s_r = 'time ' + repr(time + context_time) + 'ms:'
            run_counter = 0
            if (time < 1000):
                print(s_r, "Process", running[0].n, "(tau", running[0].tauarray[running[0].cpu_i], "ms)",
                      "started using the CPU for " + str(running[0].cpu[running[0].cpu_i]) + "ms burst [Q",
                      printNames(readyQ))            
        # Time increment and ender.
        time += 1
