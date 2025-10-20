# https://en.wikipedia.org/wiki/Discrete-event_simulation (Events List -> Last Paragraph)
# https://builtin.com/data-science/priority-queues-in-python
# https://www.geeksforgeeks.org/python/priority-queue-in-python/
# https://docs.python.org/3/library/heapq.html
# https://www.geeksforgeeks.org/python/heap-queue-or-heapq-in-python/

# heapq automatically sorts by time (priority queue)
import heapq
import numpy as np

# Output File
with open("queue_metrics.csv", "w") as f:
    f.write("rho, E[N], P_IDLE\n")

# Initialize parameters for queue
L = 12000
C = 1e6
T = 1000

# List for rho
rho_list = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]

# Loop through list
for rho in rho_list:

    # Initialize arrival, observer and departure rates
    lamda = rho * C / L
    alpha = 3 * lamda
    mu = C / L
    # rho = lamda / mu

    # Initialize simulation parameters, queues and metrics
    current_time = 0
    departure_time = 0
    queue_sum = 0
    queue_idle = 0
    queue_length = 0
    Na = 0
    Nd = 0
    No = 0
    event_list = []

    # Schedule departure using random exponential generator
    def schedule_departure(current_time, mu):
        U = np.random.uniform(0, 1)
        service_time = -np.log(1-U) / mu
        return current_time + service_time

    # Generate arrival events
    time = 0
    while (time < T):
        U = np.random.uniform(0, 1)
        time += -np.log(1-U) / lamda
        heapq.heappush(event_list, (time, "ARRIVAL"))

    # Generate observer events
    time = 0
    while (time < T):
        U = np.random.uniform(0, 1)
        time += -np.log(1-U) / alpha
        heapq.heappush(event_list, (time, "OBSERVER"))

    # Simulation
    while (event_list):
        
        # Grab next packet
        current_time, event = heapq.heappop(event_list)

        # Arrival Event
        if (event == "ARRIVAL"):
            Na += 1
            
            # If idle, schedule a departure. Else, packet joins the queue and waits
            if (current_time >= departure_time):
                departure_time = schedule_departure(current_time, mu)
                heapq.heappush(event_list, (departure_time, "DEPARTURE"))
            else:
                queue_length += 1

        # Departure Event
        elif (event == "DEPARTURE"):
            Nd += 1
            
            # If there are packets in the queue, schedule departure of the next packet. Else, set to idle
            if (queue_length > 0):
                queue_length -= 1
                departure_time = schedule_departure(current_time, mu)
                heapq.heappush(event_list, (departure_time, "DEPARTURE"))
            else:
                departure_time = current_time

        # Observer Event
        elif (event == "OBSERVER"):
            No += 1
            queue_sum += queue_length

            # If server is not busy, increment idle counter
            if (current_time >= departure_time):
                queue_idle += 1

    # Calculate metrics
    E_N = queue_sum / No
    P_IDLE = queue_idle / No
    P_LOSS = 0

    # Write metrics to file
    with open("queue_metrics.csv", "a") as f:
        f.write(f"{rho},{E_N},{P_IDLE}\n")

    # Print simulation results
    print(f"Simulation Time: {T}s")
    print(f"Averge number packets in queue (E[N]) = {E_N:.6f}")
    print(f"Proportion of time server is idle (P_IDLE) = {P_IDLE:.6f}")
    print(f"Utilization of queue (Rho) = {rho:.6f}")
    print(f"Number of arrivals (Na) = {Na}")
    print(f"Number of departures (Nd) = {Nd}")
    print(f"Number of observations (No) = {No}")
    print(f"Packet loss probability (P_LOSS) = {P_LOSS} (Infinite Buffer)\n")