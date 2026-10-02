#!/usr/bin/env python3

af_output = open("AF.txt", "w")
gt_output = open("gt_long.txt", "w")

sample_names = ["A01_62", "A01_39", "A01_63", "A01_35", "A01_31",
                 "A01_27", "A01_24", "A01_23", "A01_11", "A01_09"]

for line in open("biallelic.vcf"):
    #Skip the header lines
    if line.startswith('#'):
        continue
    #Remove new line character at the end of the line, sep by tab
    fields = line.rstrip('\n').split('\t')
    #Ignore mitochondrial chromosome
    if fields[0] =="chrM": continue
    #label the fields
    chrom = fields[0]
    pos = fields[1]
    info=fields[7]
    sample_fields = fields[9:]

    #Extract allele frequency from column
    allele_freq = info.split("AF=")[1].split(";")[0]

    #Write a file to get the allele frequency for each variant
    af_output.write(chrom + "\t" + pos + "\t" + allele_freq + "\n")

    #Write a file to get the genotype if each variant
    for sample_name, sample_field in zip(sample_names, sample_fields):
        genotype = sample_field.split(":")[0]
        gt_output.write(chrom + "\t" + pos + "\t" + sample_name + "\t" + genotype + "\n")


af_output.close()
gt_output.close()