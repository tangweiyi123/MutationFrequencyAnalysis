from Bio import SeqIO

# Define input and output file paths
input_fasta = "spikeprot1110.fasta"
output_fasta = "cleaned.fa"

def extract_sample_id(header):
    """Extract the sample ID from the header (4th field separated by '|')."""
    fields = header.split("|")
    if len(fields) >= 4:
        return fields[3].strip()  # Extract and clean sample ID
    else:
        return header  # Fallback: Return the original header if unexpected format

# Filter sequences
with open(input_fasta, "r", encoding="latin-1") as infile, open(output_fasta, "w") as outfile:
    for record in SeqIO.parse(infile, "fasta"):
        if "X" not in record.seq and len(record.seq) > 1260:
            record.id = extract_sample_id(record.description)
            record.description = ""
            SeqIO.write(record, outfile, "fasta")

