#!/bin/bash

#bedtools command to test for mutually exclusive
bedtools intersect -u -a nhek-active.bed -b nhek-repressed.bed 
    #0 overlap
bedtools intersect -u -a nhlf-active.bed -b nhlf-repressed.bed 
    #0 overlap

# regions that are active in NHEK and NHLF
bedtools intersect -a nhek-active.bed -b nhlf-active.bed | wc -l
    # 12174

# regions that are active in NHEK but not active in NHLF
bedtools intersect -v -a nhek-active.bed -b nhlf-active.bed | wc -l
    # 2405

# check if the sum of these outputs is euqal to the number of lines
    # 12174 + 2405 = 14579
wc -l nhek-active.bed
    #14013
    # no, these do not add to the original number of lines in nhek-active.bed

#  adjust the first command to only report 1 feature per overlap
bedtools intersect -u -a nhek-active.bed -b nhlf-active.bed | wc -l
    # 11608
    # check: 11608 + 2405 = 14013 

#using bedtools intersect -f 1
bedtools intersect -f 1 -a nhek-active.bed -b nhlf-active.bed | head -1
    # chr1	25558413	25559413	1_Active_Promoter	0	.	25558413	25559413
    # NHLF active feature is larger than NHEK active feature

#using bedtools intersect -F 1
bedtools intersect -F 1 -a nhek-active.bed -b nhlf-active.bed | head -1
    # chr1	19923013	19924213	1_Active_Promoter	0	.	19922613	19924613
    # NHEK active feature is larger than NHLF active feature
   
#using bedtools intersect -f 1 -F 1
bedtools intersect -f 1 -F 1 -a nhek-active.bed -b nhlf-active.bed | wc -l
    # chr1	1051137	1051537	1_Active_Promoter	0	.	1051137	1051537
    # both active sections are completely overlapped

bedtools intersect -a nhek-active.bed -b nhlf-active.bed | head -1
#chr1	19923013	19924213	1_Active_Promoter	0	.	19922613	19924613
# all active

bedtools intersect -a nhek-active.bed -b nhlf-repressed.bed | head -1
#chr1	1981140	1981540	1_Active_Promoter	0	.	1981140	1981540
# NHEK is active, NHLF is repressed
# mix of active and repressed, 3 actives, 2 repressed, 1 insulator/enhancer, 1 enhancer

bedtools intersect -a nhek-repressed.bed -b nhlf-repressed.bed | head -1
#chr1	11537413	11538213	12_Repressed	0	.	115340111538613
# all repressed



