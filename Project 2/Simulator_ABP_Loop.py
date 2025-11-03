import random
import heapq
import pandas as pd

tc = 0.0                            # Current time instant
SN = 0                              # Sending sequence number
RN = 0                              # Receiving sequence number (next expected frame)
Num_received_frames = 0             # Number of successfully received frames
Next_Expect_Frame = 0               # Same as RN
Next_Expect_ACK = 0                 # SN +1 mod 2
Type_1 = 0                          # ACK event
Type_2 = 1                          # Timeout event
Flag_forward = 0                    # Forward channel error indicator (2 = Frame Lost, 1 = Frame Error, 0 = All OK)
Flag_ACK = 0                        # Reverse channel error indicator (2 = ACK Lost, 1 = ACK Error, 0 = All OK)
Flag_timeout = -1                   # Timeout event flag
Sequence_timeout = -1               # Timeout event sequence number
Timeout = 0.0                       # Timeout time instant

H = 54 * 8                          # Header = 54 bytes
payload_length = 1500 * 8           # Payload = 1500 bytes
frame_length = H + payload_length   # Header + payload
tau = 250 * 0.001                   # Default One-way propagation delay 250ms
delta = 5 * tau                     # Default ACK timeout (5x propagation delay)
C = 5 * 1_000_000                   # Channel rate 5Mb/s
BER = 0.00001                       # Default Bit error rate
Limit = 10000                       # Max number of received packets

simu_start_time = 0.0               # Simulation start time
simu_end_time = 0.0                 # simulation end time

n = 0                               # Number of events in event list
L1 = payload_length + H             # Bit length of entire packet including header
L2 = H                              # Bit length of ACK

# Format: (event_type, event_time, error_flag, sequence_no)
# Priority queue using heapq
event_list = []

# Set Tau Value
def set_tau(new_tau):
    global tau
    tau = new_tau

# Set Delta Value
def set_delta(new_delta_over_tau):
    global delta
    delta = new_delta_over_tau * tau

# Set Bit Error Rate
def set_BER(new_BER):
    global BER
    BER = new_BER

# Insert event in chronological order using a heap queue
def insert_event(event_type, event_time, error_flag, seq_no):
    global n
    heapq.heappush(event_list, (event_type, event_time, error_flag, seq_no))
    n += 1

# Remove and return earliest event 
def delete_event():
    global n
    if (event_list):
        n -= 1
        return heapq.heappop(event_list)
    return None

# Initialize simulation parameters and insert the first timeout event
def initialization():
    global tc, Num_received_frames, simu_start_time, SN
    global Next_Expect_ACK, Next_Expect_Frame, RN
    global Timeout

    # Initialize time and counters
    tc = 0.0
    Num_received_frames = 0
    simu_start_time = tc

    # Initialize sequence numbers
    SN = 0
    Next_Expect_ACK = (SN + 1) % 2
    Next_Expect_Frame = 0
    RN = Next_Expect_Frame

    # Insert first timeout event
    tc += frame_length / C
    Timeout = tc + delta

    # Insert first timeout event
    insert_event(Type_2, Timeout, Flag_timeout, Sequence_timeout)

# Sending Function
def send(L1, L2):
    global tc, Flag_forward, Flag_ACK, RN, Num_received_frames, Next_Expect_Frame

    # Forward channel error count
    count_1 = 0
    for i in range(int(L1)):
        x = random.random()
        if (x < BER):
            count_1 += 1

    # Frame Lost
    if (count_1 >= 5):
        Flag_forward = 2
    
    # Frame Errored
    elif (0 < count_1 < 5):
        Flag_forward = 1
        tc += tau
    
    # Frame Passed
    else:
        Flag_forward = 0
        tc += tau

    # Reverse channel error count
    count_2 = 0
    for i in range(int(L2)):
        y = random.random()
        if (y < BER):
            count_2 += 1

    # ACK Lost
    if (count_2 >= 5):
        Flag_ACK = 2

    # ACK Errored
    elif (0 < count_2 < 5):
        Flag_ACK = 1
    
    # ACK Passed
    else:
        Flag_ACK = 0

    # No error on the forward channel
    if (Flag_forward == 0):
        
        # Update Next Expected Frame & set RN
        Next_Expect_Frame = (Next_Expect_Frame + 1) % 2
        RN = Next_Expect_Frame
    
        # ACK transmission timing
        tc += H / C
        tc += tau
        insert_event(Type_1, tc, Flag_ACK, RN)
    
    # Error on the forward channel
    elif (Flag_forward == 1):
        
        # ACK last correct frame
        RN = Next_Expect_Frame  
        tc += H / C
        tc += tau
        
        # Insert ACK Event
        if (Flag_ACK != 2):
            insert_event(Type_1, tc, Flag_ACK, RN)

# Main Simulation Loop
def main():
    global simu_end_time, SN, Next_Expect_ACK
    global Num_received_frames, Timeout, tc
    global Flag_timeout, Sequence_timeout

    # Initialize Simulation
    initialization()
    send(L1, L2)

    # Loop through the event list
    while (event_list):

        # Get next event
        event_type, event_time, _, seq_no = delete_event()
        tc = event_time

        # Successful ACK Frame Receieved
        if (event_type == Type_1 and seq_no == Next_Expect_ACK):
            
            # Update Sequence Numbers & Number Of Receieved Frames
            SN = (SN + 1) % 2
            Next_Expect_ACK = (SN + 1) % 2
            Num_received_frames += 1
            
            # Check if limit reached
            if (Num_received_frames >= Limit):
                simu_end_time = event_time
                break
            
            # Update Timeout
            tc = event_time + frame_length / C
            Timeout = tc + delta

            # Insert new Timeout Event & Delete Type 2 Event
            event_list[:] = [e for e in event_list if not (e[0] == Type_2 and e[2] == Sequence_timeout)]
            heapq.heapify(event_list)
            insert_event(Type_2, Timeout, Flag_timeout, Sequence_timeout)
            send(L1, L2)

        # Wrong Frame ACK Frame Receieved
        elif (event_type == Type_1 and seq_no != Next_Expect_ACK):
            
            # (Type 2 Event Already "Removed" With Getting Event)
            continue

        # Timeout Event
        elif (event_type == Type_2):
            
            # Update Timeout
            tc = event_time + frame_length / C
            Timeout = tc + delta
            
            # Resend Frame (Type 2 Event Already "Removed" With Getting Event)
            insert_event(Type_2, Timeout, Flag_timeout, Sequence_timeout)
            send(L1, L2)

    # Calculate Throughput & Simulation Time
    Total_simu_time = simu_end_time - simu_start_time
    Throughput = (Num_received_frames * payload_length) * 0.001 / Total_simu_time
    return Throughput

# Run Simulation
if __name__ == "__main__":

    # Define parameters
    tau_list = [0.005, 0.25]
    delta_over_tau_list = [2.5, 5, 7.5, 10, 12.5]
    BER_list = [0.0, 1e-5, 1e-4]

    # Store results
    results_10ms = []
    results_500ms = []

    # Run simulations for each combination of parameters
    for delta_over_tau in delta_over_tau_list:
        row_10ms = [delta_over_tau]
        row_500ms = [delta_over_tau]

        # 10ms table
        set_tau(tau_list[0])
        set_delta(delta_over_tau)
        for ber in BER_list:
            set_BER(ber)
            throughput = main()
            row_10ms.append(throughput * 1000)

        # 500ms table
        set_tau(tau_list[1])
        set_delta(delta_over_tau)
        for ber in BER_list:
            set_BER(ber)
            throughput = main()
            row_500ms.append(throughput * 1000)

        # Append results
        results_10ms.append(row_10ms)
        results_500ms.append(row_500ms)

    # Create DataFrames for better formatting
    columns = ["Δ/τ", "BER=0.0", "BER=1e-5", "BER=1e-4"]
    df_10ms = pd.DataFrame(results_10ms, columns = columns)
    df_500ms = pd.DataFrame(results_500ms, columns = columns)

    # Print 10ms table
    print("\nThroughput Results (bps) for 2τ = 10ms:")
    print("---------------------------------------------------------------")
    print(df_10ms.to_string(index = False, float_format = lambda x: f"{x:.2f}", col_space = 15))

    # Print 500ms table
    print("\nThroughput Results (bps) for 2τ = 500ms:")
    print("---------------------------------------------------------------")
    print(df_500ms.to_string(index = False, float_format = lambda x: f"{x:.2f}", col_space = 15))