import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV data
df = pd.read_csv('20250520/midterm_scores.csv')

# Subjects to plot
subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']

# Define bins (0-10, 10-20, ..., 90-100)
bins = np.arange(0, 110, 10)
bin_centers = bins[:-1] + 5  # Calculate the center of each bin

# Bar width and offset for each subject
bar_width = 10 / (len(subjects) + 1)  # Divide space for each subject
offsets = np.arange(len(subjects)) * bar_width  # Offset for each subject

# Define a color palette with distinct colors
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']

# Create the plot
plt.figure(figsize=(12, 8))

# Plot each subject as a separate bar group
for i, subject in enumerate(subjects):
    # Calculate histogram counts
    counts, _ = np.histogram(df[subject], bins=bins)
    # Plot bars with offset
    plt.bar(
        bin_centers + offsets[i],  # Offset each subject's bars
        counts,
        width=bar_width,
        label=subject,
        color=colors[i],  # Use distinct colors
        edgecolor='black',  # Add black border
        linewidth=0.1  # Set border thickness
    )

# Add labels, title, and legend
plt.title('Score Distribution by Subject (Grouped)', fontsize=16)
plt.xlabel('Score Range', fontsize=12)
plt.ylabel('Number of Students', fontsize=12)
plt.xticks(bin_centers, [f'{int(bins[i])}-{int(bins[i+1]-1)}' for i in range(len(bins)-1)])
plt.legend(title='Subjects', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()