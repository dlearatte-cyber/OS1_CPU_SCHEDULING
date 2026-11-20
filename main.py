from dataclasses import dataclass 

@dataclass
class Process:
    pid: str
    arrival: int
    burst: int

def read_processes(filename):
    processes = []

    with open(filename, "r") as file:
        for line in file:
            parts = line.split()
            if len(parts) == 3:
                pid, arrival, burst = parts
                processes.append(Process(pid, int(arrival), int(burst)))

    return processes

def fcfs(processes):
    processes = sorted(processes, key=lambda p: p.arrival)
    time = 0
    results = []
    gantt = []

    for p in processes:
        if time < p.arrival:
            gantt.append(("Idle", time, p.arrival))
            time = p.arrival

        start = time
        time += p.burst
        completion = time

        turnaround = completion - p.arrival
        waiting = turnaround - p.burst
        response = start - p.arrival

        results.append((p.pid, completion, turnaround, waiting, response))
        gantt.append((p.pid, start, completion))

    return results, gantt

def srtf(processes):
    remaining = {p.pid: p.burst for p in processes}
    time = 0
    completed = 0
    n = len(processes)
    first_start = {}
    completion_times = {}
    gantt = []
    current = None

    while completed < n:
        ready = [p for p in processes
                 if p.arrival <= time and remaining[p.pid] > 0]

        if not ready:
            if current != "Idle":
                gantt.append(("Idle", time, time + 1))
            else:
                gantt[-1] = ("Idle", gantt[-1][1], time + 1)
            current = "Idle"
            time += 1
            continue

        p = min(ready, key=lambda x: remaining[x.pid])

        if p.pid not in first_start:
            first_start[p.pid] = time

        if current != p.pid:
            gantt.append((p.pid, time, time + 1))
        else:
            gantt[-1] = (p.pid, gantt[-1][1], time + 1)

        current = p.pid
        remaining[p.pid] -= 1
        time += 1

        if remaining[p.pid] == 0:
            completion_times[p.pid] = time
            completed += 1

    results = []

    for p in processes:
        completion = completion_times[p.pid]
        turnaround = completion - p.arrival
        waiting = turnaround - p.burst
        response = first_start[p.pid] - p.arrival

        results.append((p.pid, completion, turnaround, waiting, response))

    return results, gantt

def display(name, results, gantt):
    print("\n", name)
    print("-" * 60)

    print("PID | CT | TAT | WT | RT")
    for row in results:
        print(*row, sep=" | ")

    print("\nGantt Chart:")
    for pid, start, end in gantt:
        print(f"[{start}] -- {pid} -- [{end}]")

    avg_waiting = sum(row[3] for row in results) / len(results)
    avg_turnaround = sum(row[2] for row in results) / len(results)
    avg_response = sum(row[4] for row in results) / len(results)

    print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Response Time: {avg_response:.2f}")

def main():
    processes = read_processes("input.txt")

    if not processes:
        print("No processes found!")
        return

    results1, gantt1 = fcfs(processes)
    results2, gantt2 = srtf(processes)

    display("FCFS", results1, gantt1)
    display("SRTF", results2, gantt2)

if __name__ == "__main__":
    main()
