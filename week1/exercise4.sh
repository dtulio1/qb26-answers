#!/bin/bash

bedtools intersect -c -a "hg19-kc.bed" -b "snps-chr1.bed" | sort -k5nr | head -1
# chr1	245912648	246670581	ENST00000490107.6_7	5445
# Systematic name: ENSG00000185420.20_14
# Human readable name: SMYD3
# Position: hg19 chr1:245,912,644-246,580,711 
# Size: 668,068 
# Total Exon Count: 12
# This probable has the most SNPs because the gene is so big


# Create a subset of SNPs  using bedtools sample -n 20 -seed 42
bedtools sample -n 20 -seed 42 -i snps-chr1.bed > subset.bed

# Sort the subset of SNPs
bedtools sort -i subset.bed > sorted-subset-snps.bed

# Sort hg19-kc.bed
bedtools sort -i hg19-kc.bed > sorted-hg19.bed

# How many SNPs are inside a gene?
bedtools closest -d -t first -a sorted-subset-snps.bed -b sorted-hg19.bed | cut -f 11 | grep -x "0" | wc -l
# 15

# What is the range of distances for the ones outside a gene?
bedtools closest -d -t first -a sorted-subset-snps.bed -b sorted-hg19.bed | cut -f 11   
# minimum:  1664
# maximum:  22944