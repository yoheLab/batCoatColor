# Scripts Used in the Bat Coat Color Project
Scripts used primarily to parse or transform the bat coat color dataset (a bunch of genes).


## Python Scripts

Some of these are more useful than others. Their use case as they are is pretty specific to the file structure and naming scheme of this project but they can likely be altered to serve other needs if necessary! 

### blastRenamer

This script goes through a set of fasta files and reformats the header of each fasta query present in a file. For the purposes of this project, each fasta file represented a species, containing about 1000 gene sequences/headers. This script will specifically convert headers in the following manner:

Original header:
>>ID=>Antrozous_pallidus.ENSG00000100596.8_ENST00000556607.1_SPTLC2.match_part1;Target=>Antrozous_pallidus.ENSG00000100596.8_ENST00000556607.1_SPTLC2(-)

New header:
>>Antrozous_pallidus_SPTLC2_part1_ENSG00000100596.8_ENST00000556607.1

New headers in include the following inforation from left to right:
- Species name
- gene name
- match_part number
- ensembl gene ID
- ensembl transcript ID

When changing headers, this script is designed to account for subspecies names within the data set (such as Murina_aurata_feae) and genes lacking a common name/symbol (will default to being called "noName").

To use this script, change the variable named "filePath" to correspond to a folder of fasta files. The script create a new folder called "RenamedBlastFiles" and output to it. The script will output a file for every input file.

For output file naming to work, the script expects every input file to end with ".tblastn.fa". Output names will be the same, only with ".newname" being inserted before ".tblastn.fa". 

This script is designed for windows, but can be tweaked for unix systems (change instances of "\\\\" to "/")

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

The script will also assume each file has only one fasta header and sequence.

There are two sections of commented out code.

- The first (os.rename block) is meant for moving gene files that did not have to be dedupe'd over to the output folder.
- The second is for if one would like to see the shell output of running the dedupe.sh script.

This script was designed for unix systems, though it can function on windows using WSL.

### geneSeparator

This script will take all the fasta files in a directory, and split every blast query into individual files. The individual query files are then sorted into folders, identified by the gene name and transcript ID. If the gene does not have a common name, the gene ID will be used instead. For this project, this script was used following a large BLAST query, where tblastn results were converted into a fasta format and parsed to have altered headers. 

The script works off of a root directory, with an input an output folder stemming off of it. The input directory should contain fasta files with multiple queries. The output directory be filled with folders corresponding to gene name and transcript ID as mentioned above. If the output directory was named "BaseFolder", the final file scheme will look like the example below.

>- BaseFolder
>   - FirstGeneFolder
>       - speciesOneFirstGene.fa
>       - speciesTwoFirstGene.fa
>   - SecondGeneFolder  
>       - speciesOneSecondGene.fa
>       - speciesTwoSecondGene.fa

All file path variables are located in the main method. The change the root directory, edit the "rootPath" variable. To change input/output directory, edit the "inputPath" and "outPath" respectively.

For dynamic folder and file naming to function properly, blast headers should look as follows:

>Canis_lupus_VPS18_part1_ENSG00000104142.11_ENST00000558474.1

This script is designed for windows, but can be tweaked for unix systems (change instances of "\\\\" to "/")

### humanGeneSeqGenerator

This script takes a fasta file containing multiple queries and converts them into individual files based on the folders of a dataset. For this project, human gene sequences needed to be isolated and added to the data set. So, a large fasta file was downloaded from ensembl (comprising ~2000 gene sequences) and this script was used to match those queries with the ~160 gene dataset of this project. This also served to filter out any undesired sequences from the large human fasta file. 

For this script to function, it relies on two key aspects of the data. First, for the fasta file being distributed into the data, each header follows the ensembl format for nucleotide sequences of proteins including gene ID + version, transcript ID + version, and gene symbol. An example of a header from the fasta file may be viewed below.

>>ENSG00000124795.17|ENST00000244776.11|DEK

Secondly, this script relies on the usage of this projects file system. This entails a base folder filled with folders whose names contain the gene symbol and transcript ID. See an example below.

>ACTR2_ENST00000260641.10

The script will add a query from the fasta file being broken up if it finds a folder whose gene name and transcript ID correspond with the folder name. For genes without a common gene symbol, gene ID should be used. Folder name for genes without a common symbol look as follows:

>noName_ENSG00000261832.6_ENST00000638036.1

Lastly, this is what the final file scheme should look like follow the usage of this script:

>- BaseFolder
>   - FirstGeneFolder
>       - speciesOneFirstGene.fa
>       - speciesTwoFirstGene.fa
>       - newHumanQueryFirstGene.fa
>   - SecondGeneFolder  
>       - speciesOneSecondGene.fa
>       - speciesTwoSecondGene.fa
>       - newHumanQuerySecondGene.fa

Notably this script has been coded with the purpose of using human/Homo_sapien gene sequences, but that does not mean it cannot be altered for other species. To do so, in the "writeFasta" function, change any instance of "Homo_sapien" to the desired species.

To use this script, the file paths in the main method may be changed to suit individual needs. change the "humanPath" variable to the desired input fasta file. Change the "outPath" variable to the base folder of the dataset being added to.

This script is designed for windows, but can be tweaked for unix systems (change instances of "\\\\" to "/").

### longestSeqGenerator

### transcriptCounter


## BASH Scripts

These scripts are either for file manipulation or program execution.