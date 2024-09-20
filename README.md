# Scripts Used in the Bat Coat Color Project
Scripts used primarily to parse or transform the bat coat color dataset (a bunch of genes).


## Python Scripts

Some of these are more useful than others. Their use case as they are is pretty specific to the file structure and naming scheme of this project but they can likely be altered to serve other needs if necessary! 

Some of these are more useful than others. Their use case as they are is pretty specific to the file structure and naming scheme of this project but they can likely be altered to serve other needs if necessary! 

### blastRenamer

This script goes through a set of fasta files and reformats the header of each fasta query present in a file. For the purposes of this project, each fasta file represented a species, containing about 1000 gene sequences/headers. This script will specifically convert headers in the following manner:

Original header:
>ID=>Antrozous_pallidus.ENSG00000100596.8_ENST00000556607.1_SPTLC2.match_part1;Target=>Antrozous_pallidus.ENSG00000100596.8_ENST00000556607.1_SPTLC2(-)

New header:
>Antrozous_pallidus_SPTLC2_part1_ENSG00000100596.8_ENST00000556607.1

New headers in include the following inforation from left to right:
- Species name
- gene name
- match_part number
- ensembl gene ID
- ensembl transcript ID

When changing headers, this script is designed to account for subspecies names within the data set (such as Murina_aurata_feae) and genes lacking a common name/symbol (will default to being called "noName")

To use this script, change the variable named "filePath" to correspond to a folder of fasta files. The script create a new folder called "RenamedBlastFiles" and output to it. The script will output a file for every input file.

For output file naming to work, the script expects every input file to end with ".tblastn.fa". Output names will be the same, only with ".newname" being inserted before ".tblastn.fa". 

This script is designed for windows, but can be tweaked for unix systems (change instances of "\\" to "/")

### dedupeLoop

This script was created with the purpose of comparing two fasta files together using the dedupe shell script. For this project, some genes had multiple "match_part" fasta queries/files (Queries would be labeled as "match_part1", "match_part2", "match_part3" etc.). These sequences look identical when viewed within a gene alignment program, so to determine if all match_part sequences were identical to their same gene counterpart, dedupe would be run on each match_part group and duplicated would be removed to thin the dataset. 

This script worked based on the file structure for the latter chunk of this project, which looks as follows:

>- BaseFolder
>   - FirstGeneFolder
>       - speciesOneFirstGene.fa
>       - speciesTwoFirstGene.fa
>   - SecondGeneFolder  
>       - speciesOneSecondGene.fa
>       - speciesTwoSecondGene.fa

When utilizing the script, the "inputFolder" variable/directory should be set to the base directory as shown in the file system above. The "outputFolder" variable/directory can be set to wherever. The "dedupePath" variable should be set to wherever the user has "dedupe.sh" stored on their PC (this script can be acquired online through bbtools).

The script will start at the baseFolder and pull fasta file names from each sub folder. The script will count the number of entries in the folders per species. The script assumes that if there is more than one than one entry per species within a folder, that multiple match_part entries are present. Otherwise, the script will ignore the subfolder and continue onto the next folder. Notably, the script operates off of files with the following naming scheme:

>Aeorestes_cinereus.ACTR2_ENSG00000138071.15_ENST00000377982.8.fa

The script will also assume each file has only one fasta header and sequence

There are two sections of commented out code

- The first (os.rename block) is meant for moving gene files that did not have to be dedupe'd over to the output folder
- The second is for if one would like to see the shell output of running the dedupe.sh script


### geneSeparater

### humanGeneSeqGenerator

### longestSeqGenerator

### transcriptCounter


## BASH Scripts

These scripts are either for file manipulation or program execution.