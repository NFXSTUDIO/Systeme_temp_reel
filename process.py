import heapq

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0

def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)  # Trier par ordre d'arrivée
    time = 0
    results = []
    total_waiting_time = 0
    
    for process in processes:
        if time < process.arrival_time:
            time = process.arrival_time  # Attendre si nécessaire
        process.waiting_time = time - process.arrival_time
        process.turnaround_time = process.waiting_time + process.burst_time
        total_waiting_time += process.waiting_time
        results.append((process.pid, time, time + process.burst_time))
        time += process.burst_time
    
    performances = total_waiting_time / len(processes)
    return results, performances