#!/bin/bash

# make windows command
# bedtools makewindows -g hg16-main.chrom.sizes -w 1000000 > hg16-1mb.bed

# intersect command
# bedtools intersect -c -a hg16-1mb.bed -b hg16-kc.bed > hg16-kc-count.bed

#How many genes are in hg19?
wc -l hg19-kc.bed
    # 80309 (80308 genes because of the header line)

#How many genes are in hg19 but not in hg16?
bedtools intersect -v -a hg19-kc.bed -b hg16-kc.bed > unique_hg19-kc.bed | wc - l
    #42737

#Why are some genes in hg19 but not hg16?
    #genome assemblies improve over time, so hg19 could have resolved gaps
    #or errors in hg16, resulting in more genes being identiied


#How many genes are in hg16?
wc -l hg16-kc.bed 
    #21365 (21364 because of the header line)

#How many genes are in hg16 but not in hg19
bedtools intersect -v -a hg16-kc.bed -b hg19-kc.bed| wc -l
    #3458

#Why are some genes in hg16 but not in hg19?
    #as an earlier iteration, hg16 could have interpetted some repeats or gaps
    #in regions as a seperate gene, but then this problem was fixed in hg19