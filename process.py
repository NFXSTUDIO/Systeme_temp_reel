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

def sjn_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)  # Tri par ordre d'arrivée
    time = 0
    results = []
    index = 0
    total_waiting_time = 0
    ready_queue = []  # Initialisation de la file d'attente prête

    while index < len(processes) or ready_queue:
        # Ajouter les processus arrivés à la file d'attente
        while index < len(processes) and processes[index].arrival_time <= time:
            heapq.heappush(ready_queue, (processes[index].burst_time, processes[index]))  # Ajouter par temps d'exécution (burst time)
            index += 1

        if ready_queue:
            burst_time, process = heapq.heappop(ready_queue)
            process.waiting_time = time - process.arrival_time
            process.turnaround_time = process.waiting_time + process.burst_time
            total_waiting_time += process.waiting_time
            results.append((process.pid, time, time + process.burst_time))
            time += process.burst_time
        elif index < len(processes):
            time = processes[index].arrival_time  # Sauter au prochain processus si la file est vide et des processus arrivent

    performances = total_waiting_time / len(processes)
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