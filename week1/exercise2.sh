#!/bin/bash

# make windows command
# bedtools makewindows -g hg16-main.chrom.sizes -w 1000000 > hg16-1mb.bed

# intersect command
# bedtools intersect -c -a hg16-1mb.bed -b hg16-kc.bed > hg16-kc-count.bed

#How many genes are in hg19?
wc -l hg19-kc-count.bed

#How many genes are in hg19 but not in hg16?
bedtools intersect -v -a hg19-kc-count.bed -b hg16-kc-count.bed | wc -l

#Why are some genes in hg19 but not hg16?
    #genome assemblies improve over time, so hg19 could have resolved gaps
    #or errors in hg16, resulting in more genes being identiied


#How many genes are in hg16?
wc -l hg16-kc-count.bed 

#How many genes are in hg16 but not in hg19
bedtools intersect -v -b hg19-kc-count.bed -a hg16-kc-count.bed | wc -l

#Why are some genes in hg16 but not in hg19?
    #as an earlier iteration, hg16 could have interpetted some repeats or gaps
    #in regions as a seperate gene, but then this problem was fixed in hg19