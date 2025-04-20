import pandas as pd

# Load the mutation frequency file
input_file = "mutation_frequency.csv"
output_file = "simplified_mutation_frequency.csv"

# Read the CSV file
mutation_data = pd.read_csv(input_file)

# Combine mutations by position, summing frequencies
simplified_data = mutation_data.groupby("Position", as_index=False).agg({"Frequency": "sum"})

# Sort by position in ascending order
simplified_data = simplified_data.sort_values(by="Position", ascending=True)

# Save the simplified data to a new CSV file
simplified_data.to_csv(output_file, index=False)
print(f"Simplified mutation frequency data saved to {output_file}")
