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
    print(processes)
    processes.sort(key=lambda x: x.arrival_time)  # sort per arrival
    time = 0
    results = []
    total_waiting_time = 0
    start_time = 0
    
    processes.sort(key=lambda x: x.arrival_time)
    
    for process in processes:
        if time >= process.arrival_time:
            start_time = time
            while process.remaining_time > 0:
                time += 1
                process.remaining_time -= 1
            if process.remaining_time == 0:
                process.waiting_time = time - process.arrival_time
                process.turnaround_time = process.waiting_time + process.burst_time
                total_waiting_time += process.waiting_time
                results.append((process.pid, start_time, time))
    
    performances = total_waiting_time / len(processes)
    return results, time, performances

def sjn_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    ready_queue = []
    time = 0
    results = []
    index = 0
    total_waiting_time = 0

    while index < len(processes) or ready_queue:
        while index < len(processes) and processes[index].arrival_time <= time:
            heapq.heappush(ready_queue, (processes[index].burst_time, processes[index]))
            index += 1

        if ready_queue:
            _, process = heapq.heappop(ready_queue)
            process.waiting_time = time - process.arrival_time
            process.turnaround_time = process.waiting_time + process.burst_time
            total_waiting_time += process.waiting_time
            results.append((process.pid, time, time + process.burst_time))
            time += process.burst_time
        else:
            time = processes[index].arrival_time

    performances = total_waiting_time / len(processes)
    return results, time, performances

def rr_scheduling(processes, quantum=4):
    time = 0
    results = []
    ready_queue = deque()
    total_waiting_time = 0
    completed = 0
    n = len(processes)

    for p in processes:
        p.remaining_time = p.burst_time

    processes.sort(key=lambda x: x.arrival_time)
    index = 0

    while completed != n:
        while index < n and processes[index].arrival_time <= time:
            ready_queue.append(processes[index])
            index += 1

        if not ready_queue:
            time += 1
            continue

        process = ready_queue.popleft()
        start_time = time

        if process.remaining_time <= quantum:
            time += process.remaining_time
            process.remaining_time = 0
            process.waiting_time = time - process.arrival_time - process.burst_time
            process.turnaround_time = time - process.arrival_time
            total_waiting_time += process.waiting_time
            results.append((process.pid, start_time, time))                
            completed += 1
        else:
            time += quantum
            process.remaining_time -= quantum
            results.append((process.pid, start_time, time))

        while index < n and processes[index].arrival_time <= time:
            if processes[index] not in ready_queue and processes[index].remaining_time > 0:
                ready_queue.append(processes[index])
                index += 1

        if process.remaining_time > 0:
            ready_queue.append(process)

    performances = total_waiting_time / n
    return results, time, performances

def rm_scheduling(processes): 
    time = 0
    results = []
    ready_queue = []
    total_waiting_time = 0
    start_time = 0
    
    hyperperiod = max([p.period for p in processes if p.period]) * 2  # simulation jusqu'à une certaine limite
    processes.sort(key=lambda x: x.period)  # sort per period
    temp_pid = processes[0].pid
    temp_st_time = processes[0].arrival_time
    temp_time = processes[0].arrival_time
    temp_remaining_time = processes[0].remaining_time
    # Initialize the ready queue with the process that arrive at time 0
    for p in processes:
            if (time - p.arrival_time) % p.period == 0 and time >= p.arrival_time:
                new_instance = Process(p.pid, time, p.burst_time, p.period)
                heapq.heappush(ready_queue, (new_instance.period, new_instance))
    print(ready_queue)

    print("debut traitement : ")
    while time < hyperperiod:
        # Ajouter les réapparitions périodiques
        for p in processes:
            if (time - p.period) % p.period == 0 and time > p.arrival_time:
                new_instance = Process(p.pid, time, p.burst_time, p.period)
                #print("time when the process is created",time)
                heapq.heappush(ready_queue, (new_instance.period, new_instance))
        #print(ready_queue)
        if ready_queue:
            _, process = heapq.heappop(ready_queue)
            if process.pid != temp_pid and temp_remaining_time > 0: # if the previous process is not the same as the current one we save it in the results
                results.append((temp_pid, temp_st_time, temp_time))
                start_time = 0
            if start_time == 0:
                start_time = time
            time += 1
            process.remaining_time -= 1
            temp_remaining_time = process.remaining_time

            if process.remaining_time == 0:
                process.turnaround_time = time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                total_waiting_time += process.waiting_time
                results.append((process.pid, start_time, time))
                start_time = 0
            else:
                temp_pid = process.pid
                temp_st_time = start_time
                temp_time = time
                heapq.heappush(ready_queue, (process.period, process))
        else:
            time += 1

    performances = total_waiting_time / len(processes)
    return results, time, performances

def edf_scheduling(processes):
    time = 0
    results = []
    ready_queue = []
    total_waiting_time = 0
    start_time = 0

    hyperperiod = max([p.deadline for p in processes if p.deadline]) * 2
    for p in processes:
        if p.arrival_time == 0:
            new_instance = Process(p.pid, time, p.burst_time, deadline=p.deadline)
            heapq.heappush(ready_queue, (new_instance.deadline, new_instance))

    while time < hyperperiod:
        for p in processes:
            if time > p.arrival_time and (time - p.arrival_time) % p.period == 0:
                new_instance = Process(p.pid, time, p.burst_time, deadline=time + p.deadline)
                heapq.heappush(ready_queue, (new_instance.deadline, new_instance))

        # Remove expired processes
        ready_queue = [(d, p) for d, p in ready_queue if time < p.deadline]
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
                results.append((process.pid, start_time, time))
                start_time = 0
            else:
                heapq.heappush(ready_queue, (process.deadline, process))
        else:
            time += 1

    performances = total_waiting_time / len(processes)
    return results, time, performances

if __name__ == "__main__":
    # test exemple
    processes = [
        Process(1, 1, 5),
        Process(2, 1, 3),
        Process(3, 2, 8),
    ]
    print("FCFS Scheduling:")
    fcfs_results, time, fcfs_avg_wait = fcfs_scheduling(processes)
    print(fcfs_results)
    print("Average Waiting Time:", fcfs_avg_wait)

    print("\nSJN Scheduling:")
    sjn_results,time, sjn_avg_wait = sjn_scheduling(processes)
    print(sjn_results)
    print("Average Waiting Time:", sjn_avg_wait)

    print("\nRR Scheduling:")
    rr_results, time, rr_avg_wait = rr_scheduling(processes)
    print(rr_results)
    print("Average Waiting Time:", rr_avg_wait)
    
    processes1 = [
        Process(1, 0, 1, 4),
        Process(2, 0, 2, 5),  
        Process(3, 0, 3, 10),  
    ]
    print("\nRM Scheduling:")
    rm_results, rm_tt_time, rm_avg_wait = rm_scheduling(processes1)
    print(rm_results)
    print("Time:", rm_tt_time)
    print("Average Waiting Time:", rm_avg_wait)

    processes2 = [
        Process(1, 0, 3, 20, 7),
        Process(2, 0, 2, 5, 4), 
        Process(3, 0, 2, 10, 8), 
    ]
    print("\nEDF Scheduling:")
    edf_results, time, edf_avg_wait = edf_scheduling(processes2)
    print(edf_results)
    print("Average Waiting Time:", edf_avg_wait)