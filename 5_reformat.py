import math

# Open the input file and read its lines
with open('MutationRateAttr_Raw.txt', 'r') as file:
    lines = file.readlines()

# Open the output file for writing
with open('output.txt', 'w') as file:
    for line in lines:
        key, value = map(int, line.strip().split(','))  # Split by comma and convert to integers
        new_value = round(math.log10(value), 1)
        file.write(f"\t:{key}\t{new_value}\n")  # Write in the desired format
