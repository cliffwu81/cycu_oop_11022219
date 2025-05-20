import pandas as pd

# Load CSV data
df = pd.read_csv('20250520/midterm_scores.csv')

subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']
total_subjects = len(subjects)

# Create a list to store disqualified students
disqualified_students = []

for idx, row in df.iterrows():
    failed_count = sum(row[subj] < 60 for subj in subjects)
    if failed_count >= total_subjects / 2:
        disqualified_students.append(row)

# Convert the list of disqualified students to a DataFrame
disqualified_df = pd.DataFrame(disqualified_students)

# Save the DataFrame to a CSV file
output_path = '20250520/disqualified_students.csv'
disqualified_df.to_csv(output_path, index=False)

print(f"Disqualified students have been saved to {output_path}")