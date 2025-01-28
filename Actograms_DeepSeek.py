# Use the script below to make the intenisty-based actograms
import matplotlib.pyplot as plt
import numpy as np

# Simulated activity data (e.g., 7 days of 24-hour data)
days = 7
hours = 24
activity_data = np.random.randint(0, 10, size=(days, hours))  # 7 days, 24 hours

# Create the actogram
fig, ax = plt.subplots(figsize=(10, 6))

# Plot each day's activity
for i, day in enumerate(activity_data):
    for j, activity in enumerate(day):
        ax.barh(y=i, width=1, height=0.8, left=j, color='black', alpha=activity / 10)  # Activity bars

# Customize the plot
ax.set_yticks(np.arange(days))
ax.set_yticklabels([f'Day {i+1}' for i in range(days)])
ax.set_xlabel('Time (Hours)')
ax.set_ylabel('Days')
ax.set_title('Actogram of Simulated Activity Data')
ax.set_xlim(0, hours)
ax.set_ylim(-0.5, days - 0.5)

plt.show()

# Use the script below to make the vertical lines actograms
import matplotlib.pyplot as plt
import numpy as np

# Simulated activity data (e.g., 7 days of 24-hour data)
days = 7
hours = 24
activity_data = np.random.randint(0, 10, size=(days, hours))  # 7 days, 24 hours

# Create the actogram
fig, ax = plt.subplots(figsize=(10, 6))

# Plot each day's activity as vertical lines
for i, day in enumerate(activity_data):
    for j, activity in enumerate(day):
        if activity > 0:  # Only plot if there is activity
            ax.vlines(x=j, ymin=i, ymax=i + (activity / 10), color='black', linewidth=1)

# Customize the plot
ax.set_yticks(np.arange(days) + 0.5)  # Center labels between days
ax.set_yticklabels([f'Day {i+1}' for i in range(days)])
ax.set_xlabel('Time (Hours)')
ax.set_ylabel('Days')
ax.set_title('Actogram of Simulated Activity Data')
ax.set_xlim(0, hours)
ax.set_ylim(0, days)

# Add light-dark cycle shading (optional)
for j in range(hours):
    if j < 12:  # Light period (e.g., 6 AM to 6 PM)
        ax.axvspan(j, j + 1, color='yellow', alpha=0.1)
    else:  # Dark period (e.g., 6 PM to 6 AM)
        ax.axvspan(j, j + 1, color='gray', alpha=0.1)

plt.show()