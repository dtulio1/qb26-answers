#!/usr/bin/env python3

import sys
import fasta

file = open( sys.argv[1] )
genomes = fasta.FASTAReader( file )

contigs_number = 0
total_length = 0
for ident, sequence in genomes:
    contigs_number += 1
    seq_length = len(sequence)
    total_length += int(seq_length)

avg_length = total_length / int(contigs_number)
print("Number of contigs: ", contigs_number, "Total length: ", total_length, "Average length: ", avg_length)
    

file.close()


# iterate through FASTAReader using for ident, sequence in__
# count the number of contigs
# determine the sequence length using len() and sum up the total length
# print the "Number of contigs: ", "Total length: ", and "Average length: "
