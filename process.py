import time as t
import numpy as np
class Process:
    def __init__(self, pid, arrival_time, burst_time, period=None, deadline=None):
        self.pid = pid                      # id of the process
        self.arrival_time = arrival_time    # time of the arrival
        self.burst_time = burst_time        # execution time
        self.remaining_time = burst_time    # time left before the end of execution
        self.waiting_time = 0               # waiting time
        self.turnaround_time = 0            # time between the arrival and the end of the execution
        self.period = period
        self.deadline = deadline

def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    ready_queue = [] # list : [pid, enter_time , -10(null value)] & [pid, -10(null value), leave_time]
    ready_list = [] # list that contains [pid, start_time, end_time]
    time = 0
    results = []
    cpu = []
    total_waiting_time = 0
    completed = 0
    start_time = 0
    n = len(processes)

    # while all the process hasn't been processed
    while completed != n:
        # arrived process                   first apparition
        arrived = [p for p in processes if p.arrival_time <= time]
    
        for p in arrived:
            # print("process :", p.pid, "arrivée à", time)
            ready_queue.append(p)                               # add it to the ready_queue
            ready_list.append([p.pid, time, -10])               # mark it as arrived
            processes.remove(p)                                 # remove the process from the list of processes if it's add to the ready queue
        
        # if there is process in the queue or in the cpu
        if ready_queue != [] or cpu != []:
            
            # if there is no process cpu
            if cpu == []:
                process = ready_queue.pop(0)                        # take the first process in the ready_queue
                cpu.append(process.pid)                             # add the process to the cpu
                ready_list.append([process.pid, -10, time])         # add to read_list the process that is currently processing
                start_time = time                                   # we reset the start time

            # if the process is finished 
            if process.remaining_time == 0: 
                process.waiting_time = time - process.arrival_time
                total_waiting_time += process.waiting_time
                results.append([process.pid, start_time, time]) # we add it to the results
                cpu.pop()                                       # remove the process from the cpu       
                start_time = time                               # reset the start time
                completed += 1                                  # increment the number of completed processes
            
            # if the process is not finished
            else:                           
                process.remaining_time -= 1                     # decrement the remaining time
                time += 1                                       # increment the time
        else:
            time += 1

    performances = total_waiting_time / n
    return results, time, performances, ready_list

def sjn_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    ready_queue = [] # list : [pid, enter_time , -10(null value)] & [pid, -10(null value), leave_time]
    ready_list = [] # list that contains [pid, start_time, end_time]
    time = 0
    cpu = []
    results = []
    total_waiting_time = 0
    completed = 0
    start_time = 0
    n = len(processes)

    # while all the process hasn't been processed
    while completed != n:
        # arrived process                   first apparition
        arrived = [p for p in processes if p.arrival_time <= time]
        for p in arrived:
            ready_queue.append(p)                               # add it to the queue
            ready_queue.sort(key=lambda x: x.burst_time)        # sort the ready queue by remaining time
            ready_list.append([p.pid, time, -10])               # mark it as finished
            processes.remove(p)                                 # remove the process from the list

        # if there is process in the queue
        if ready_queue != [] or cpu != []:

            # if there is no process cpu
            if cpu == []:
                process = ready_queue.pop(0)                    # take the first process in the ready_queue
                cpu.append(process.pid)                         # add the process to the cpu
                ready_list.append([process.pid, -10, time])     # add to read_list the process that is currently processing
                start_time = time                               # we reset the start time
            
            # if the process is finished 
            if process.remaining_time == 0: 
                process.waiting_time = time - process.arrival_time
                total_waiting_time += process.waiting_time
                results.append([process.pid, start_time, time]) # we add it to the results
                cpu.pop()                                       # remove the process from the cpu
                start_time = time                               # increment the time
                completed += 1                                  # increment the number of completed processes
            
            # if the process is not finished
            else:                           
                process.remaining_time -= 1                     # decrement the remaining time
                time += 1                                       # increment the time
        else:
            time += 1

    performances = total_waiting_time / n
    return results, time, performances, ready_list

def rr_scheduling(processes, quantum=4):
    processes.sort(key=lambda x: x.arrival_time)
    ready_queue = [] # list : [pid, enter_time , -10(null value)] & [pid, -10(null value), leave_time]
    ready_list = [] # list that contains [pid, start_time, end_time]
    time = 0
    cpu = [] # list that contains the process that is currently processing
    results = []
    total_waiting_time = 0
    completed = 0
    start_time = 0
    n = len(processes)
    temp_q = quantum

    # while all the process hasn't been processed
    while completed != n:
        # arrived process                   first apparition
        arrived = [p for p in processes if p.arrival_time <= time]
        for p in arrived:
            ready_queue.append(p)                               # add it to the queue
            ready_list.append([p.pid, time, -10])               # mark it as finished
            processes.remove(p)                                 # remove the process from the list 
        
        # if there is process in the queue or in the cpu
        if ready_queue != [] or cpu != []:
            
            # if there is no process cpu
            if cpu == []:
                process = ready_queue.pop(0)                        # take the first process in the ready_queue
                cpu.append(process.pid)                             # add the process to the cpu
                ready_list.append([process.pid, -10, time])         # add to read_list the process that is currently processing
                start_time = time                                   # we reset the start time

            # if the process is finished 
            if process.remaining_time == 0: 
                process.waiting_time = time - process.arrival_time
                total_waiting_time += process.waiting_time
                results.append([process.pid, start_time, time]) # we add it to the results
                cpu.pop()                                       # remove the process from the cpu       
                start_time = time                               # reset the start time
                completed += 1                                  # increment the number of completed processes
                temp_q = quantum                                # reset the quantum
                
            # if the quantum is finished
            elif temp_q == 0:               
                process.arrival = time                          # set the arrival time to the current time
                results.append([process.pid, start_time, time]) # add it to the results
                ready_queue.append(process)                     # add it at the ready_queue
                ready_list.append([process.pid, time, -10])     # add to read_list the process that is currently processing 
                cpu.pop()                                       # remove the process from the cpu
                start_time = time                               # reset the start time
                temp_q = quantum                                # reset the quantum
            
            else:                           
                process.remaining_time -= 1                     # decrement the remaining time
                temp_q -= 1                                     # decrement the quantum
                time += 1                                       # increment the time
        else:
            time += 1

    performances = total_waiting_time / n
    return results, time, performances, ready_list

def rm_scheduling(processes): 
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    cpu = [] # list that contains the process that is currently processing
    results = []
    ready_queue = [] # list : [pid, enter_time , -10(null value)] & [pid, -10(null value), leave_time]
    ready_list = [] # list that contains [pid, start_time, end_time]
    total_waiting_time = 0
    start_time = 0
    STOP = False

    # time limit
    hyperperiod = np.lcm.reduce([p.period for p in processes if p.period]) # hyperperiod = LCM of all periods
    
    while time < hyperperiod:
        if STOP == False:
            # arrived process                       first apparition                    periodic apparition
            arrived = [p for p in processes if (time == p.arrival_time or (time - p.arrival_time) % p.period == 0)]
            # print("time",time)
            for p in arrived:
                # print("process :", p.pid, "arrivée à", time)
                new_instance = Process(p.pid, time, p.burst_time, p.period) # create a new process
                ready_queue.append(new_instance)                            # add it to the ready_queue
                ready_queue.sort(key=lambda x: x.period)                    # sort the list
                ready_list.append([new_instance.pid, time, -10])            # mark it as arrived
            # print("coucou1")
        STOP = False
        # if there is process in the queue or in the cpu
        if ready_queue != [] or cpu != []:
            
            # if there is no process cpu
            if cpu == []:
                process = ready_queue.pop(0)                        # take the first process in the ready_queue
                cpu.append(process.pid)                             # add the process to the cpu
                ready_list.append([process.pid, -10, time])         # add to read_list the process that is currently processing
                start_time = time                                   # we reset the start time
                # print("check cpu")            

            # if the process is finished 
            if process.remaining_time == 0: 
                process.waiting_time = time - process.arrival_time
                total_waiting_time += process.waiting_time
                results.append([process.pid, start_time, time]) # we add it to the results
                cpu.pop()                                       # remove the process from the cpu       
                start_time = time                               # reset the start time
                # print("check finish")
                STOP = True

            # if there is a process with a shorter period than the current one
            elif any(p.period < process.period for p in ready_queue):
                # print("process :", process.pid, " qui est retiré, period :",process.period)
                results.append([process.pid, start_time, time])     # we add the current one in the results
                ready_queue.append(process)                         # we add the current one in the ready_queue
                ready_queue.sort(key=lambda x: x.period)                # we sort the list to have the first element with the shortest period
                ready_list.append([process.pid, -10, time])             # add the process that came back in the ready_queue
                cpu.pop()                                               # remove the process from the cpu
                start_time = time                                       # reset the start time
                # print("check1 inf-period", process.pid)
                STOP = True

            else:
                process.remaining_time -= 1                             # decrement the remaining time
                time += 1                                               # increment the time
                # print("check indent")
        else:
            time += 1                                                   # increment the time

    performances = total_waiting_time / len(processes)
    return results, time, performances, ready_list

def edf_scheduling(processes): 
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    cpu = [] # list that contains the process that is currently processing
    results = []
    ready_queue = [] # list : [pid, enter_time , -10(null value)] & [pid, -10(null value), leave_time]
    ready_list = [] # list that contains [pid, start_time, end_time]
    total_waiting_time = 0
    start_time = 0
    STOP = False

    # time limit
    hyperperiod = np.lcm.reduce([p.period for p in processes if p.period]) # hyperperiod = LCM of all periods
    
    while time < hyperperiod:
        if STOP == False:
            # arrived process                       first apparition                    periodic apparition
            arrived = [p for p in processes if (time == p.arrival_time or (time - p.arrival_time) % p.period == 0)]
            for p in arrived:
                new_instance = Process(p.pid, time, p.burst_time, p.period) # create a new process
                ready_queue.append(new_instance)                            # add it to the ready_queue
                ready_queue.sort(key=lambda x: x.deadline)                    # sort the list
                ready_list.append([new_instance.pid, time, -10])            # mark it as arrived
                # print("ready list (arrivée):", ready_list)
        STOP = False
        # if there is process in the queue or in the cpu
        if ready_queue != [] or cpu != []:
            
            # loop to look for a process 
            for p in ready_queue:
                # if the process reaches its deadline
                if p.deadline == time:
                    ready_queue.remove(p)                           # we erase it
                    ready_list.append([p.pid, -10, time])           # we mark it as leaving the queue
            
            # if there is no process cpu
            if cpu == []:
                process = ready_queue.pop(0)                        # take the first process in the ready_queue
                cpu.append(process.pid)                             # add the process to the cpu
                ready_list.append([process.pid, -10, time])         # add to read_list the process that is currently processing
                start_time = time                                   # we reset the start time

            # if the process is finished 
            if process.remaining_time == 0: 
                process.waiting_time = time - process.arrival_time
                total_waiting_time += process.waiting_time
                results.append([process.pid, start_time, time]) # we add it to the results
                cpu.pop()                                       # remove the process from the cpu       
                start_time = time                               # reset the start time
                STOP = True

            # if there is a process with a shorter deadline than the curreznt one
            elif any(p.deadline < process.deadline for p in ready_queue):
                results.append([process.pid, start_time, time])     # we add the current one in the results
                ready_queue.append(process)                         # we add the current one in the ready_queue
                ready_queue.sort(key=lambda x: x.deadline)          # we sort the list to have the first element with the shortest period
                ready_list.append([process.pid, -10, time])         # add the process that came back in the ready_queue
                cpu.pop()                                       # remove the process from the cpu
                start_time = time                               # reset the start time
                # print("ready list (retour):", ready_list)
                STOP = True
            
            else:
                process.remaining_time -= 1                         # decrement the remaining time
                time += 1
        else:
            time += 1

    performances = total_waiting_time / len(processes)
    return results, time, performances, ready_list

if __name__ == "__main__":
    # test exemple
    processes = [
        Process(1, 1, 5),
        Process(2, 1, 3),
        Process(3, 2, 8),
    ]
    # print("FCFS Scheduling:")
    # fcfs_results, time, fcfs_avg_wait, rd_list = fcfs_scheduling(processes)
    # print(fcfs_results)
    # print("Ready List:", rd_list)
    # print("Average Waiting Time:", fcfs_avg_wait)

    processes = [
        Process(1, 1, 5),
        Process(2, 1, 3),
        Process(3, 2, 8),
    ]
    # print("\nSJN Scheduling:")
    # sjn_results,time, sjn_avg_wait, rd_list = sjn_scheduling(processes)
    # print(sjn_results)
    # print("Ready List:", rd_list)
    # print("Average Waiting Time:", sjn_avg_wait)

    processes = [
        Process(1, 1, 5),
        Process(2, 1, 3),
        Process(3, 2, 8),
    ]
    # print("\nRR Scheduling:")
    # rr_results, time, rr_avg_wait, rd_list = rr_scheduling(processes)
    # print(rr_results)
    # print("Ready List:", rd_list)
    # print("Average Waiting Time:", rr_avg_wait)
    
    processes1 = [
        Process(1, 0, 1, 4),
        Process(2, 0, 2, 5),  
        Process(3, 0, 3, 10),  
    ]
    # print("\nRM Scheduling:")
    # rm_results, rm_tt_time, rm_avg_wait, rd_list = rm_scheduling(processes1)
    # print(rm_results)
    # print("Ready List:", rd_list)
    # # print("Time:", rm_tt_time)
    # print("Average Waiting Time:", rm_avg_wait)

    processes2 = [
        Process(1, 0, 3, 20, 7),
        Process(2, 0, 2, 5, 4), 
        Process(3, 0, 2, 10, 8), 
    ]
    print("\nEDF Scheduling:")
    edf_results, time, edf_avg_wait, rd_list = edf_scheduling(processes2)
    print(edf_results)
    print("Ready List:", rd_list)
    print("Average Waiting Time:", edf_avg_wait)