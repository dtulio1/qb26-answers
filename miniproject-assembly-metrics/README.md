# Mini Project Assembly Metrics

Compared C. remanei assemblies

## File URLs and uncompressed file size
- PRJNA247909: https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS19/species/caenorhabditis_remanei/PRJNA248909/caenorhabditis_remanei.PRJNA248909.WBPS19.genomic.fa.gz (uncomopressed file size: 115M)
- PRJNA248911: https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS19/species/caenorhabditis_remanei/PRJNA248911/caenorhabditis_remanei.PRJNA248911.WBPS19.genomic.fa.gz (uncompressed file size: 121M)
- PRJNA53697: https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS19/species/caenorhabditis_remanei/PRJNA53967/caenorhabditis_remanei.PRJNA53967.WBPS19.genomic.fa.gz (uncompressed file size: 141M)
- PRJNA577507: https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/releases/WBPS19/species/caenorhabditis_remanei/PRJNA577507/caenorhabditis_remanei.PRJNA577507.WBPS19.genomic.fa.gz (uncompressed file size: 127M)

-------
## instructions on how to use assembly-metrics.py
This script gives the number of contigs, total length, and average length for a .fa file (.fa.gz files must be unzipped)

### How to run these scripts:
Pass these scripts as arguments through the command line
- Note: make sure all scripts are made executable before running (chmod +/ SCRIPTNAME)
- To execute scripts: ./SCRIPTNAME
 
 1) Use the getGenomes.sh to download the fasta files
  * Unzip using gunzip *.gz
 2) Store assembly-metrics.py and your unzipped files in the same directory
 3) Execute assembly-metrics.py in the command line, using your genome file name as the 1th argument
    * ex. ./assembly-metrics.py genome_file1.fa
- Execute the script for each fasta file.

-------
## assembly-metrics.py results
- PRJNA247909 (Year: 2014) 
    * Number of contigs:  1591 
    * Total length:  118549266 
    * Average length:  74512.42363293526
- PRJNA248911 (Year: 2015)
    * Number of contigs:  912 
    * Total length:  124541912 
    * Average length:  136559.11403508772
- PRJNA53697
    * Number of contigs:  3670 
    * Total length:  145442736 
    * Average length:  39630.17329700272
- PRJNA577507 (2019): 
    * Number of contigs:  187 
    * Total length:  130480874 
    * Average length:  697758.6844919786

### trends
- Based off the results, it appears that new genome assemblies have fewer contigs and instead, a larger average length. The number of contigs decreased drastically from 1591 to 187 across 5 years. It also appears that total length appeared to increase over time. However, PRJNA5367 is not included in this analysis as there is no year currently available.