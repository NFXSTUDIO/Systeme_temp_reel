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

def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)  # sort per arrival
    time = 0
    results = []
    total_waiting_time = 0
    
    for process in processes:
        if time < process.arrival_time:
            time = process.arrival_time  # wait if we have to
        process.waiting_time = time - process.arrival_time
        process.turnaround_time = process.waiting_time + process.burst_time
        total_waiting_time += process.waiting_time
        results.append((process.pid, time, time + process.burst_time))
        time += process.burst_time
    
    performances = total_waiting_time / len(processes)
    return results, performances

def sjn_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time) 
    time = 0
    results = []
    index = 0
    total_waiting_time = 0
    ready_queue = []  # ready_queue initialize
    n = len(processes)

    while index < n or ready_queue:
        # Add the processes to the queue
        while index < n and processes[index].arrival_time <= time:
            heapq.heappush(ready_queue, (processes[index].burst_time, processes[index]))  # add per burst time
            index += 1

        if ready_queue:
            burst_time, process = heapq.heappop(ready_queue)
            process.waiting_time = time - process.arrival_time
            process.turnaround_time = process.waiting_time + process.burst_time
            total_waiting_time += process.waiting_time
            results.append((process.pid, time, time + process.burst_time))
            time += process.burst_time
        elif index < n:
            time = processes[index].arrival_time  # switch to the next process if the ready queue is empty and the process arrive

    performances = total_waiting_time / n
    return results, performances

def rr_scheduling(processes, quantum=4): # devault value of quantum
    time = 0
    results = []
    ready_queue = deque()
    total_waiting_time = 0
    completed = 0
    n = len(processes)

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

        if process.remaining_time <= quantum:
            time += process.remaining_time
            process.remaining_time = 0
            process.waiting_time = time - process.arrival_time - process.burst_time
            process.turnaround_time = time - process.arrival_time
            total_waiting_time += process.waiting_time
            results.append((process.pid, time - process.burst_time, time))
            completed += 1
        else:
            time += quantum
            process.remaining_time -= quantum
            ready_queue.append(process)

        if process.remaining_time > 0:
            if index < n:
                for p in processes[index:]:
                    if p.arrival_time <= time and p not in ready_queue and p.remaining_time > 0:
                        ready_queue.append(p)
            for p in processes:
                if p.arrival_time <= time and p not in ready_queue and p.remaining_time > 0:
                    ready_queue.append(p)

    performances = total_waiting_time / n
    return results, performances

def rm_scheduling(processes): 
    time = 0
    results = []
    ready_queue = []
    total_waiting_time = 0
    completed = 0
    n = len(processes)

    processes.sort(key=lambda x: x.arrival_time)
    index = 0

    while completed != n:
        # Add the processes to the queue
        while index < n and processes[index].arrival_time <= time:
            heapq.heappush(ready_queue, (1 / processes[index].period, processes[index]))
            index += 1

        if not ready_queue:
            time += 1
            continue

        _, process = heapq.heappop(ready_queue)

        time += process.remaining_time
        process.remaining_time = 0
        process.waiting_time = max(0, time - process.arrival_time - process.burst_time)
        process.turnaround_time = time - process.arrival_time
        total_waiting_time += process.waiting_time
        results.append((process.pid, time - process.burst_time, time))
        completed += 1

        for p in processes:
            if p.pid == process.pid:
                p.arrival_time = time
                p.deadline = time + p.period
                p.remaining_time = p.burst_time
                if p.arrival_time <= time :
                  heapq.heappush(ready_queue, (1 / p.period, p))
                break

    performances = total_waiting_time / n
    return results, performances

def edf_scheduling(processes):
    time = 0
    results = []
    ready_queue = []  # Renommé pour plus de clarté
    total_waiting_time = 0
    completed = 0
    n = len(processes)

    processes.sort(key=lambda x: x.arrival_time)
    index = 0

    while completed != n:
        while index < n and processes[index].arrival_time <= time:
            heapq.heappush(ready_queue, (processes[index].deadline, processes[index]))
            index += 1

        if not ready_queue:
            time += 1
            continue

        _, process = heapq.heappop(ready_queue)

        time += process.remaining_time
        process.remaining_time = 0
        process.waiting_time = time - process.arrival_time - process.burst_time 
        process.turnaround_time = time - process.arrival_time
        total_waiting_time += process.waiting_time
        results.append((process.pid, time - process.burst_time, time))
        completed += 1

        for p in processes:
            if p.pid == process.pid:
                p.arrival_time = time
                p.deadline = time + p.period
                p.remaining_time = p.burst_time
                if p.arrival_time <= time:
                    heapq.heappush(ready_queue, (p.deadline, p))
                break

    performances = total_waiting_time / n
    return results, performances

if __name__ == "__main__":
    # test exemple
    processes = [
        Process(1, 0, 5),
        Process(2, 1, 3),
        Process(3, 2, 8),
        Process(4, 3, 6)
    ]
    print("FCFS Scheduling:")
    fcfs_results, fcfs_avg_wait = fcfs_scheduling(processes)
    print(fcfs_results)
    print("Average Waiting Time:", fcfs_avg_wait)

    print("\nSJN Scheduling:")
    sjn_results, sjn_avg_wait = sjn_scheduling(processes)
    print(sjn_results)
    print("Average Waiting Time:", sjn_avg_wait)

    print("\nRR Scheduling:")
    rr_results, rr_avg_wait = rr_scheduling(processes)
    print(rr_results)
    print("Average Waiting Time:", rr_avg_wait)
    
    processes1 = [
        Process(1, 0, 3, 10),
        Process(2, 2, 4, 15),  
        Process(3, 4, 5, 20),  
    ]
    print("\nRM Scheduling:")
    rm_results, rm_avg_wait = rm_scheduling(processes1)
    print(rm_results)
    print("Average Waiting Time:", rm_avg_wait)

    processes2 = [
        Process(1, 0, 3, 10, 10),
        Process(2, 2, 4, 15, 15), # Process 2 arrive plus tard
        Process(3, 4, 5, 20, 20), # process 3 arrive encore plus tard
    ]
    print("\nEDF Scheduling:")
    edf_results, edf_avg_wait = edf_scheduling(processes2)
    print(edf_results)
    print("Average Waiting Time:", edf_avg_wait)