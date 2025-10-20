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

    # Initialize simulation parameters, queues and metrics
    current_time = 0
    departure_time = 0
    queue_sum = 0
    server_idle = 0
    queue_length = 0
    Na = 0
    Nd = 0
    No = 0
    event_list = []
    arrival_list = []
    departure_list = []

    # Schedule departure using random exponential generator
    def generate_service_time(mu):
        U = np.random.uniform(0, 1)
        service_time = -np.log(1-U) / mu
        return service_time

    # Generate arrival events
    time = 0
    while (time < T):
        U = np.random.uniform(0, 1)
        time += -np.log(1-U) / lamda
        arrival_list.append(time)
        heapq.heappush(event_list, (time, "ARRIVAL"))

    # Generate departure events
    for i in range(len(arrival_list)):
        if(i == 0):
            departure_list.append(arrival_list[i] + generate_service_time(mu))
        elif(departure_list[i-1] > arrival_list[i]):
            departure_list.append(departure_list[i-1] + generate_service_time(mu))
        elif(departure_list[i-1] <= arrival_list[i]):
            departure_list.append(arrival_list[i] + generate_service_time(mu))  

    # Push departure times to event list
    for departure_time in departure_list:
        heapq.heappush(event_list, (departure_time, "DEPARTURE"))

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

        # Departure Event
        elif (event == "DEPARTURE"):
            Nd += 1
        
        # Observer Event
        elif (event == "OBSERVER"):
            No += 1

            # If something is in the system
            if(Na - Nd > 0):
                queue_sum += Na - Nd - 1

            # If server is not busy, increment idle counter
            if (Na - Nd == 0):
                server_idle += 1

    # Calculate metrics
    E_N = queue_sum / No
    P_IDLE = server_idle / No
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