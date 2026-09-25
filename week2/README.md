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
 bwa mem -t 4 -R "@RG\tID:A01_23\tSM:$A01_23" ../genomes/sacCer3.fa ~/Data/BYxRM/fastq/A01_23.fq.gz > A01_23.sam
