import pandas as pd
from collections import Counter

# Input and output file paths
input_file = "mutations.txt"
output_file = "mutation_frequency.csv"

# Parse the mutation data
mutation_data = []

with open(input_file, "r") as file:
    for line in file:
        sample_id, mutations = line.strip().split("\t")
        for mutation in mutations.split(","):
            position = "".join([char for char in mutation if char.isdigit()])
            change = mutation.replace(position, "")
            mutation_data.append((position, change))

# Count frequencies
mutation_counter = Counter(mutation_data)

# Reformat to a DataFrame
mutation_frequency = pd.DataFrame(
    [(pos, mut, count) for (pos, mut), count in mutation_counter.items()],
    columns=["Position", "Mutation", "Frequency"],
)

# Save to CSV
mutation_frequency.to_csv(output_file, index=False)
print(f"Mutation frequency data saved to {output_file}")
