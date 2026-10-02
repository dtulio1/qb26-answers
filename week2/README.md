# Exercise 1

## Question 1 Bash commands 

**Preparation**
To unzip the BYxRM.tar:
    tar xvf BYxRM.tar 

**Step 1.1**
cd genomes
cp ~/Data/References/sacCer3/sacCer3.fa.gz .
gunzip sacCer3.fa.gz
bwa index sacCer3.fa

****Step 1.2**
cd ../variants
bwa mem -t 4 -R "@RG\tID:A01_09\tSM:A01_09" ../genomes/sacCer3.fa ~/Data/BYxRM/fastq/A01_09.fq.gz > A01_09.sam

**Step 1.3**
samtools sort -@ 4 -O bam -o A01_09.bam A01_09.sam
samtools index A01_09.bam

**Step 1.4**
For loop example
for my_sample in A01_09 A01_11 A01_23
do
    echo "Now processing" ${my_sample}
done

## Exercise 1 Questions

**Question 1.1**
   - File sizes:
       - .fq.gz  41M
       - .bam 47M
       - .bam.bai 32K
       - .sam 166M
   - The .fq.gz file is compressed with gzip, versus the .sam file is uncompressed. The .sam file aso stores other alignment metadata that is not found in the .fq file.

   - The .bam file is the compressed binary format of a .sam file. Since it is compressed, it makes sense that it is a lot smaller than the .sam file.

**Question 1.2**
- bwa mem -t 4 -R "@RG\tID:A01_23\tSM:$A01_23" ../genomes/sacCer3.fa ~/Data/BYxRM/fastq/A01_23.fq.gz > A01_23.sam

# Exercise 2

## Exercise 2 Bash commands

**Step 2.1** 
samtools view -H A01_09.bam

**Step 2.2**
- samtools view A01_09.bam | head -n 3
- Output: 
- HWI-ST387_0114:5:47:16737:7355#0	0	chrI	29	60	76M	*	0	0	ACACCACACACCACACCACACCCACACACACACATCCTAACACTACCCTAACACAGCCCTAATCTAACCCTGGCCA	@FGDFGFGGDGGGGHHGHEHHHGHHHGFHHFFDC>DEEEEDDB< BE>?7?>C@@@@CDBDDF?E2FBDAA>361::	NM:i:0	MD:Z:76	AS:i:76	XS:i:22	RG:Z:A01_09
HWI-ST387_0114:5:23:10710:84112#0	0	chrI	47	60	76M	*	0	0	CACCCACACACACACATCCTAACACTACCCTAACACAGCCCTAATCTAACCCTGGCCAACCTGTCTCTCAACTTAC	BE8E=EGGFGFEEFEFGGGFCFFFFD?BDDDDFEBD:A?A:ED=BDA?ADD28..8:>6>;6>??BFDED.DAEBE	NM:i:0	MD:Z:76	AS:i:76	XS:i:0	RG:Z:A01_09
HWI-ST387_0114:5:42:14962:12601#0	16	chrI	47	60	4S72M	*	0	0	ACAGCACCCACACACACACATCCTAACACTACCCTAACACAGTCCTAATCTAACCCTGGCCAACCTGTCTCTCAAC	###############BB>B@.CAAC<9;@61=A>/BADAD:E;FECDFCB=FCFGFAGFGG@DFGEFFFDEDGGGE	NM:i:1	MD:Z:38C33	AS:i:67	XS:i:26	RG:Z:A01_09

**Step 2.3** 
samtools flagstat A01_09.bam > A01_09.flagstat
cat A01_09.flagstat

## Exercise 2 Questions

**Question 2.1**
- The @SQ lines give you an SN and an LN. The SN gives you the sequence name, or in this case, the chromosome. The LN gives you the length of the sequence.
- There are 17 @SQ lines

**Question 2.2**
- Looking at the first alignment, it aligned to chromosome 1, at position 29. It's CIGAR score is 76M, indicating 76 matches.

**Question 2.3**
- The @RG and RG:Z comes from the ID and SM that we attributed to this sample when indexing. The RG:Z is a tag, specifying that this specific read belongs to that sample/read group. Therefore, each read needs to carry a tag so it can be assigned to that group/sample.

**Question 2.4**
- 100% of reads mapped to the reference genome. This is suspicious because you would expect some sort of interference whether with sample quality or differences across yeast samples.

**Question 2.5**
- These zeroes are telling you that no mate exists and their is no mate to pair it with. This tells you that it was single-end sequencing rather than paired-end sequencing.

**Question 2.6**
- It appears that AO1_24, A01_34, A01_62, and A01_63 carry BY ancestry.
- It appears that A01_09, A01_11, A01_23, A01_27, A01_35, A01_39 carry RM ancestry.
- Yes, it appears the visual call agrees with the published genotypes.
    - ex: grep -F -e 'chr01_27915' -e 'chr01_28323' -e 'chr01_28652' -e 'chr01_29667' ~/Data/BYxRM/BYxRM_GenoData.txt | cut -f 63
        - returned B for all

# Exercise 2

## Exercise 2 Questions

**Question 3.1**
- The last 10 columns are our samples. These are pulled from the sample name that is within each BAM file.
- The ploidy argument matters because these yeast segregants are haploid. If it was diploid it would show two numbers as the genotype, like 0/1 instead of either just 1 or 0. You would need to run -p 2.

