import pandas as pd
import matplotlib.pyplot as plt

# Read CSV as dataframe
df_metrics = pd.read_csv("queue_metrics.csv")

#-----E[N]-----#

# Setup Figure
plt.figure(figsize = (10, 6))

# Plot Rho vs E[N]
plt.bar(df_metrics["rho"], df_metrics[" E[N]"], label = "Averge Number Of Packets In Queue E[N]", width = 0.05)

# Assign labels and other options for the plot
plt.xlabel("Queue Utilization (ρ)")
plt.ylabel("Averge Number Of Packets In Queue E[N]")
plt.title("Queue Utilization (ρ) vs Averge Number Of Packets In Queue E[N]")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

#-----P_IDLE-----#

# Setup Figure
plt.figure(figsize = (10, 6))

# Plot Rho vs E[N]
plt.bar(df_metrics["rho"], df_metrics[" P_IDLE"], label = "Proportion Of Time Server Is Idle P_IDLE", width = 0.05)

# Assign labels and other options for the plot
plt.xlabel("Queue Utilization (ρ)")
plt.ylabel("Proportion Of Time Server Is Idle P_IDLE")
plt.title("Queue Utilization (ρ) vs Proportion Of Time Server Is Idle P_IDLE")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()