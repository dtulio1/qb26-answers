#!/bin/bash

# the 10 segregants we will analyze
for my_sample in A01_09 A01_11 A01_23 A01_24 A01_27 A01_31 A01_35 A01_39 A01_62 A01_63
do
    echo "***" ${my_sample}

    # align reads to the reference genome
    bwa mem -t 4 -R "@RG\tID:${my_sample}\tSM:${my_sample}" ../genomes/sacCer3.fa ~/Data/BYxRM/fastq/${my_sample}.fq.gz > ${my_sample}.sam

    # sort the alignments by position and convert to BAM
    samtools sort -@ 4 -O bam -o ${my_sample}.bam ${my_sample}.sam

    # index the BAM file
    samtools index ${my_sample}.bam
done
