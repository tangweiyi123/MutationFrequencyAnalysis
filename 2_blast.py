import os
import time
from Bio import SeqIO
from multiprocessing import Pool, cpu_count

# File paths
input_fasta = "cleaned.fa"
reference_db = "reference_db"  # DIAMOND reference database (created using diamond makedb)
output_file = "mutations.txt"
processed_log = "processed.log"

# Function to run DIAMOND for a single sequence
def process_sequence(record):
    """Run DIAMOND on a single sequence and extract mutations."""
    temp_query = f"temp_{record.id}.fasta"  # Temporary file for the query sequence
    
    # Write the sequence to a temporary file
    with open(temp_query, "w") as temp_file:
        SeqIO.write(record, temp_file, "fasta")

    try:
        # Run DIAMOND
        temp_output = f"temp_{record.id}.out"
        command = [
            "diamond", "blastp",
            "--query", temp_query,
            "--db", reference_db,
            "--out", temp_output,
            "--outfmt", "6 qseqid sseqid qstart sstart qseq_gapped sseq_gapped",
            "--gapopen", "11",  # Gap opening penalty (default in BLASTp)
            "--gapextend", "1",  # Gap extension penalty (default in BLASTp)
            "--more-sensitive",  # Increase sensitivity for better gap handling
	    "--masking", "0",
	    "--quiet",
        ]
        os.system(" ".join(command))

        # Parse DIAMOND output
        mutations = []
        if os.path.exists(temp_output):
            with open(temp_output, "r") as f:
                for line in f:
                    _, _, q_start, s_start, query_seq, subject_seq = line.strip().split("\t")
                    q_start, s_start = int(q_start), int(s_start)
                    for i, (q_aa, s_aa) in enumerate(zip(query_seq, subject_seq)):
                        if q_aa != s_aa:
                            pos = s_start + i
                            if q_aa == "-":  # Gap in query
                                mutations.append(f"{s_aa}{pos}-")
                            elif s_aa == "-":  # Gap in subject
                                mutations.append(f"-{pos}{q_aa}")
                            else:  # Mismatch
                                mutations.append(f"{s_aa}{pos}{q_aa}")

        # Write result immediately
        if mutations:
            with open(output_file, "a") as out_file:
                out_file.write(f"{record.id}\t{','.join(mutations)}\n")
            log_processed_id(record.id)

        # Clean up temporary files
        os.remove(temp_query)
        os.remove(temp_output)

        return record.id  # Return ID for tracking progress

    except Exception as e:
        print(f"Error processing {record.id}: {e}")
        os.remove(temp_query)
        if os.path.exists(temp_output):
            os.remove(temp_output)
        return None

# Load processed sequence IDs
def load_processed_ids():
    if os.path.exists(processed_log):
        with open(processed_log, "r") as log_file:
            return set(line.strip() for line in log_file)
    return set()

# Save processed ID
def log_processed_id(record_id):
    with open(processed_log, "a") as log_file:
        log_file.write(f"{record_id}\n")

# Parallel processing function
def process_sequences_in_parallel(records, num_processes):
    with Pool(processes=num_processes) as pool:
        for result in pool.imap_unordered(process_sequence, records):
            if result:
                print(f"Processed: {result}")  # Real-time progress

# Main script
if __name__ == "__main__":
    # Start time tracking
    start_time = time.time()

    # Load processed IDs
    processed_ids = load_processed_ids()

    # Filter sequences to process
    with open(input_fasta, "r") as infile:
        records_to_process = [record for record in SeqIO.parse(infile, "fasta") if record.id not in processed_ids]
    
    print(f"Processing {len(records_to_process)} sequences out of {len(processed_ids) + len(records_to_process)} total.")

    # Specify the number of parallel processes (adjust this value as needed)
    num_parallel_processes = 10  # You can increase this based on your system's resources

    # Process sequences in parallel
    process_sequences_in_parallel(records_to_process, num_parallel_processes)
    
    # End time tracking
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTotal time taken: {elapsed_time:.2f} seconds")
