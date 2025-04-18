import heapq
from collections import deque

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
# pb quand commence pas a 0
def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    ready_queue = []
    ready_list = [] # list that contains [pid, start_time, end_time]
    time = 0
    results = []
    total_waiting_time = 0
    completed = 0
    start_time = 0
    n = len(processes)
    temp_pid = -1

    while completed != n:
        arrived = [p for p in processes if p.arrival_time <= time]
        for p in arrived:
            ready_queue.append(p)
            ready_list.append([p.pid, time, None])
            processes.remove(p) # remove the process from the list of processes if it's add to the ready queue
                
        if ready_queue:
            process = ready_queue.pop(0)
            if process.pid != temp_pid:     # if the previous process is not the same as the current one
                start_time = time                               # we reset the start time
            if process.remaining_time == 0: # if the process is finished 
                process.waiting_time = time - process.arrival_time
                total_waiting_time += process.waiting_time
                results.append([process.pid, start_time, time]) # we add it to the results
                ready_list.append([process.pid, None, time])    # we mark it as finished in the ready queue
                start_time = 0                                  # reset the start time
                completed += 1                                  # increment the number of completed processes
            else:                           # if the process is not finished
                process.remaining_time -= 1                     # decrement the remaining time
                ready_queue.insert(0,process)                   # add it back to the ready queue
                temp_pid = process.pid                          # we save the current process id
                time += 1                                       # increment the time
        else:
            time += 1

    performances = total_waiting_time / n
    return results, time, performances, ready_list

def sjn_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    ready_queue = []
    ready_list = [] # list that contains [pid, start_time, end_time]
    time = 0
    results = []
    total_waiting_time = 0
    completed = 0
    start_time = 0
    n = len(processes)
    temp_pid = -1

    while completed != n:
        arrived = [p for p in processes if p.arrival_time <= time]
        for p in arrived:
            ready_queue.append(p)
            ready_queue.sort(key=lambda x: x.burst_time) # sort the ready queue by remaining time
            ready_list.append([p.pid, time, None])
            processes.remove(p) # remove the process from the list of processes if it's add to the ready queue
                
        if ready_queue:
            process = ready_queue.pop(0)
            if process.pid != temp_pid:     # if the previous process is not the same as the current one
                start_time = time                               # we reset the start time
            if process.remaining_time == 0: # if the process is finished 
                process.waiting_time = time - process.arrival_time
                total_waiting_time += process.waiting_time
                results.append([process.pid, start_time, time]) # we add it to the results
                ready_list.append([process.pid, None, time])    # we mark it as finished in the ready queue
                start_time = 0                                   # increment the time
                completed += 1                                  # increment the number of completed processes
            else:                           # if the process is not finished
                process.remaining_time -= 1                     # decrement the remaining time
                ready_queue.insert(0,process)                   # add it back to the ready queue
                temp_pid = process.pid                          # we save the current process id
                time += 1                                       # increment the time
        else:
            time += 1

    performances = total_waiting_time / n
    return results, time, performances, ready_list

def rr_scheduling(processes, quantum=4):
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    results = []
    ready_queue = deque()
    ready_list = [] # list that contains [pid, start_time, end_time]
    total_waiting_time = 0
    completed = 0
    n = len(processes)

    for p in processes:
        p.remaining_time = p.burst_time

    index = 0

    while completed != n:
        while index < n and processes[index].arrival_time <= time:
            ready_queue.append(processes[index])
            ready_list.append([processes[index].pid, time, None])
            index += 1

        if not ready_queue:
            time += 1
            continue

        process = ready_queue.popleft()
        ready_list.append([process.pid, None, time])
        start_time = time

        if process.remaining_time <= quantum:
            time += process.remaining_time
            process.remaining_time = 0
            process.waiting_time = time - process.arrival_time - process.burst_time
            process.turnaround_time = time - process.arrival_time
            total_waiting_time += process.waiting_time
            results.append([process.pid, start_time, time])                
            completed += 1
        else:
            time += quantum
            process.remaining_time -= quantum
            results.append([process.pid, start_time, time])

        while index < n and processes[index].arrival_time <= time:
            if processes[index] not in ready_queue and processes[index].remaining_time > 0:
                ready_queue.append(processes[index])
                ready_list.append([processes[index].pid, time, None])
                index += 1

        if process.remaining_time > 0:
            ready_queue.append(process)
            ready_list.append([process.pid, time, None])

    performances = total_waiting_time / n
    return results, time, performances, ready_list

def rm_scheduling(processes): 
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    results = []
    ready_queue = []
    ready_list = [] # list that contains [pid, start_time, end_time]
    total_waiting_time = 0
    start_time = 0
    
    hyperperiod = max([p.period for p in processes if p.period]) * 2  # simulation jusqu'à une certaine limite
    processes.sort(key=lambda x: x.period)  # sort per period
    temp_pid = processes[0].pid
    temp_st_time = processes[0].arrival_time
    temp_time = processes[0].arrival_time
    temp_remaining_time = processes[0].remaining_time
    temp_pro = None

    # Initialize the ready queue with the process that arrive at time 0
    for p in processes:
            if (time - p.arrival_time) % p.period == 0 and time >= p.arrival_time:
                new_instance = Process(p.pid, time, p.burst_time, p.period)
                heapq.heappush(ready_queue, (new_instance.period, new_instance))
                ready_list.append([p.pid, time, None]) # time when the process enter the ready queue

    while time < hyperperiod:
        # Ajouter les réapparitions périodiques
        for p in processes:
            if (time - p.period) % p.period == 0 and time > p.arrival_time:
                new_instance = Process(p.pid, time, p.burst_time, p.period)
                heapq.heappush(ready_queue, (new_instance.period, new_instance))
                ready_list.append([p.pid, time, None]) # time when the process enter the ready queue again
        if ready_queue:
            _, process = heapq.heappop(ready_queue)
            ready_list.append([process.pid, None, time])                # time when the process leave the ready queue     
            if process.pid != temp_pid and temp_remaining_time > 0: # if the previous process is not the same as the current one
                ready_list.append([temp_pid, None, temp_time])          # we mark the previous proc as finished in the ready queue
                results.append([temp_pid, temp_st_time, temp_time])     # we add the previous one to the results
                start_time = time                                       # set the start time to the actual time
            if start_time == 0:
                start_time = time
            time += 1
            process.remaining_time -= 1
            temp_remaining_time = process.remaining_time

            if process.remaining_time == 0:
                process.turnaround_time = time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                total_waiting_time += process.waiting_time
                results.append([process.pid, start_time, time])
                start_time = 0
            else:
                temp_pid = process.pid
                temp_st_time = start_time
                temp_time = time
                heapq.heappush(ready_queue, (process.period, process))
        else:
            time += 1

    performances = total_waiting_time / len(processes)
    return results, time, performances, ready_list

def edf_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    time = 0
    results = []
    ready_queue = []
    ready_list = [] # list that contains [pid, start_time, end_time]
    total_waiting_time = 0
    start_time = 0

    hyperperiod = max([p.deadline for p in processes if p.deadline]) * 2
    for p in processes:
        if p.arrival_time == 0:
            new_instance = Process(p.pid, time, p.burst_time, deadline=p.deadline)
            heapq.heappush(ready_queue, (new_instance.deadline, new_instance))
            ready_list.append([p.pid, time, None])

    while time < hyperperiod:
        for p in processes:
            if time > p.arrival_time and (time - p.arrival_time) % p.period == 0:
                new_instance = Process(p.pid, time, p.burst_time, deadline=time + p.deadline)
                heapq.heappush(ready_queue, (new_instance.deadline, new_instance))
                ready_list.append([p.pid, time, None])

        # Remove expired processes
        for d,p in ready_queue:
            if time < (p.arrival_time + p.deadline):
                ready_queue = [(d, p)]
            else:
                ready_list.append([p.pid, None, -1]) # minus one for expired process
        heapq.heapify(ready_queue)

        if ready_queue:
            _, process = heapq.heappop(ready_queue)
            if start_time == 0:
                start_time = time
            time += 1
            process.remaining_time -= 1

            if process.remaining_time == 0:
                process.turnaround_time = time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                total_waiting_time += process.waiting_time
                results.append([process.pid, start_time, time])
                ready_list.append([process.pid, None, time])
                start_time = 0
            else:
                heapq.heappush(ready_queue, (process.deadline, process))
                ready_list.append([process.pid, time, None])
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
    print("FCFS Scheduling:")
    fcfs_results, time, fcfs_avg_wait, rd_list = fcfs_scheduling(processes)
    print(fcfs_results)
    print("Ready List:", rd_list)
    print("Average Waiting Time:", fcfs_avg_wait)

    processes = [
        Process(1, 1, 5),
        Process(2, 1, 3),
        Process(3, 2, 8),
    ]
    print("\nSJN Scheduling:")
    sjn_results,time, sjn_avg_wait, rd_list = sjn_scheduling(processes)
    print(sjn_results)
    print("Ready List:", rd_list)
    print("Average Waiting Time:", sjn_avg_wait)

    processes = [
        Process(1, 1, 5),
        Process(2, 1, 3),
        Process(3, 2, 8),
    ]
    print("\nRR Scheduling:")
    rr_results, time, rr_avg_wait, rd_list = rr_scheduling(processes)
    print(rr_results)
    print("Ready List:", rd_list)
    print("Average Waiting Time:", rr_avg_wait)
    
    processes1 = [
        Process(1, 0, 1, 4),
        Process(2, 0, 2, 5),  
        Process(3, 0, 3, 10),  
    ]
    print("\nRM Scheduling:")
    rm_results, rm_tt_time, rm_avg_wait, rd_list = rm_scheduling(processes1)
    print(rm_results)
    print("Ready List:", rd_list)
    # print("Time:", rm_tt_time)
    print("Average Waiting Time:", rm_avg_wait)

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