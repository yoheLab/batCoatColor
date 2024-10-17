# Scripts Used in the Bat Coat Color Project
Scripts used primarily to parse or transform the bat coat color dataset (a bunch of genes).


## Python Scripts

Some of these are more useful than others. Their use case as they are is pretty specific to the file structure and naming scheme of this project but they can likely be altered to serve other needs if necessary! 

### addSpeciesName

This script was created for adding the species name to a corresponding fasta query header. This script was designed for use after processing blast data (blast -> blast2gff -> bedtools -> this script). This means the script assumes headers look like the following:

>ID=ENSG00000104142.11_ENST00000220509.10_VPS18.match_part1;Target=ENSG00000104142.11_ENST00000220509.10_VPS18(+)

The script will output the following header in response:

>ID=>Eonycteris_spelaea.ENSG00000104142.11_ENST00000220509.10_VPS18.match_part1;Target=ENSG00000104142.11_ENST00000220509.10_VPS18(+)

This script gets species names from the name of the fasta file being read. Input fasta files are named as follows:

>Eonycteris_spelaea.tblastn.fa

This script was written due to a need to add species names to blast queries prior to using the geneSeparator script. Otherwise there would be no way to know what species a sequence resulted from. 

To use this script, alter the filePath variable to be the file path of the desired input director. The script will output will output in the directory above that one with the same name as the input directory, but including "WithSpecies" in the name

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

When changing headers, this script is designed to account for subspecies names within the data set (such as Murina_aurata_feae) and genes lacking a common name/symbol (will default to being called "noName").

To use this script, change the variable named "filePath" to correspond to a folder of fasta files. The script create a new folder called "RenamedBlastFiles" and output to it. The script will output a file for every input file.

For output file naming to work, the script expects every input file to end with ".tblastn.fa". Output names will be the same, only with ".newname" being inserted before ".tblastn.fa". 

This script is designed for windows, but can be tweaked for unix systems (change instances of "\\\\" to "/")

### blastTopHits

This is a multipurpose script for altering tblastn files (output format 6) that was written and continually added to. This means it can serve multiple purposes. Some of those purposes include:
- Tracking the number of queries with invalid sequences of a fasta file (either "Sequence Missing" or nothing)
- Altering the header column of a tblastn file (output format 6)
- Selecting the top blast hits for each transcript in a file (based on e-value)
- Swapping out headers to include an additional piece of information (might be a niche usage case)

To track the number of queries with invalid sequences, use the fastaReader method and include countMissing=True. This will return two things: a dictionary representation of a fasta file (header key, sequence value), and a list of headers whose sequence was either missing or read as "Sequence Unavailable". This is useful for validating if all desired genes have a corresponding sequence. The dictionary fasta file also has applications with the headerExchange method discussed later.

At this point it is also useful to mention the fileFinder method. This method loops through all subfolders present in a directory and automatically invokes (depending on what is specified) either headerShift, headerExchange, or blastFindTopHit. An example file structure will be shown below. To use this method, alter the subFolders variable to be an attribute that each folder name has in common. For this example "Genes" will be used.

>- BaseFolder (specified in the directoryPath variable)
>   - Genes1to100
>       - speciesOne.fa
>       - speciesTwo.fa
>   - Genes101to200  
>       - speciesOne.fa
>       - speciesTwo.fa

Using the headerShift method allows for alteration of the header portion of a tblastn file (the first column). This method is not the best way to tackle this problem from this repository, so it is recommended that one finishes going through the blast processing steps and altering fasta headers using the blastRenamer.py script. That being said, this script will attempt to construct a clean header fasta from the originals in the column. It will also include a number corresponding to header's position in the file. It should be noted that the logic that builds the new header only works for a particular header format and does not account for many exceptions. The script assumes input headers look like the example below:

>ID=>Antrozous_pallidus.ENSG00000100596.8_ENST00000556607.1_SPTLC2.match_part1;Target=>Antrozous_pallidus.ENSG00000100596.8_ENST00000556607.1_SPTLC2(-)

Many will likely find the most useful part of this script using the blastFindTopHit method. This part of the script should be used right after a blast job is completed and before any processing steps. It will go through a tblastn file and isolate the top hit (based on e-value) for every gene/transcript present in the file. I have found that typically blast hits for the same gene are already organized from best to worst, but this method will check all of them just to be sure.

The final use of this script involves the "headerExchange" method. This method swaps out the headers in a tblastn file with headers that have been read into the transcriptDict in the main method. This script works by matching old headers with the new ones. Old headers are broken down and reassembled into what a new header would look like. If a a match exists, then the old header is replaced with the new one. This is especially useful if the new header contains new information not present in the old headers. It can also be used to dynamically remove information from old headers by having the new headers not include that info.

This script was designed for unix system, but could potentially be changed to work on windows. It could also likely be run using WSL on windows.

### dedupeLoop

This script was created with the purpose of comparing two fasta files together using the dedupe shell script. For this project, some genes had multiple "match_part" fasta queries/files (Queries would be labeled as "match_part1", "match_part2", "match_part3" etc.). These sequences look identical when viewed within a gene alignment program, so to determine if all match_part sequences were identical to their same gene counterpart, dedupe would be run on each match_part group and duplicates would be removed to thin the dataset. 

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

- The first (os.rename block) is meant for moving gene files that did not have to be dedupe'd over to the output folder. To use this, first uncomment the code. Then, go to the second for loop of the main method and edit the if statement (line 79) switch the "if len(speciesSortedFolderFiles[x]) **>** 1:" to "if len(speciesSortedFolderFiles[x]) **==** 1:". Lastly, comment out the "result = " statement in the dedupe method (line 33).
- The second is for if one would like to see the shell output of running the dedupe.sh script.

This script was designed for unix systems, though it can function on windows using WSL.

### fixHeaderGeneName

This is a small script that was written to fix the gene name within file names. This script loops through all files within each subfolder or a base folder and changes the gene names based upon the names of the subfolders. An example may look as follows:

Before:
>- BaseFolder
>   - OCA2_ENST00000354638.8
>       - Desmodus_rotundus.MEGATRON_ENSG00000104044.16_ENST00000354638.8
>       - Eptesicus_fuscus.MEGATRON_ENSG00000104044.16_ENST00000354638.8
>   - QKI_ENST00000361195.6
>       - Desmodus_rotundus.GOKU_ENSG00000112531.17_ENST00000361195.6
>       - Eptesicus_fuscus.GOKU_ENSG00000112531.17_ENST00000361195.6

After:
>- BaseFolder
>   - OCA2_ENST00000354638.8
>       - Desmodus_rotundus.OCA2_ENSG00000104044.16_ENST00000354638.8
>       - Eptesicus_fuscus.OCA2_ENSG00000104044.16_ENST00000354638.8
>   - QKI_ENST00000361195.6
>       - Desmodus_rotundus.QKI_ENSG00000112531.17_ENST00000361195.6
>       - Eptesicus_fuscus.QKI_ENSG00000112531.17_ENST00000361195.6

To use this script, edit the baseFolder variable to be the desired input directory file path

This script is designed for windows, but can be tweaked for unix systems (change instances of "\\\\" to "/")

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

### genesHitCounter

This script is used for creating a bar graph representing a set of genes and the number of species found to have a blast hit for each gene. This is represented as a horizontal bar plot. The genes with the most species/hits are at the top of the horizontal bar plot and vice versa.

To use this script, set baseFolderPath to the folder containing each gene subfolder. This script works off of a file similar to the one shown below:

>- BaseFolder
>   - FirstGeneFolder
>       - speciesOneFirstGene.fa
>       - speciesTwoFirstGene.fa
>   - SecondGeneFolder  
>       - speciesOneSecondGene.fa
>       - speciesTwoSecondGene.fa

The number of fasta files will be counted in each gene folder and then those results will be characterized in a graph.

This script is designed for windows, but can be tweaked for unix systems (change instances of "\\\\" to "/")

### humanGeneSeqGenerator

This script takes a fasta file containing multiple queries and converts them into individual files based on the folders of a dataset. For this project, human gene sequences needed to be isolated and added to the data set. So, a large fasta file was downloaded from ensembl (comprising ~2000 gene sequences) and this script was used to match those queries with the ~160 gene dataset of this project. This also served to filter out any undesired sequences from the large human fasta file. 

For this script to function, it relies on two key aspects of the data. First, for the fasta file being distributed into the data, each header follows the ensembl format for nucleotide sequences of proteins including gene ID + version, transcript ID + version, and gene symbol. An example of a header from the fasta file may be viewed below.

>ENSG00000124795.17|ENST00000244776.11|DEK

Secondly, this script relies on the usage of this projects file system. This entails a base folder filled with folders whose names contain the gene symbol and transcript ID. See an example below.

>ACTR2_ENST00000260641.10

The script will add a query from the fasta file being broken up if it finds a folder whose gene name and transcript ID correspond with the folder name. For genes without a common gene symbol, gene ID should be used. Folder name for genes without a common symbol look as follows:

>noName_ENSG00000261832.6_ENST00000638036.1

Lastly, this is what the final file scheme should look like following the usage of this script:

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

This script served a fairly specific purpose within this project. It goes through a list of folders containing multiple fasta sequences and calculates the average sequence length of each folder. The average sequence length of each folder is then compared to folders with sequences of the same gene, the the folder with the longest gene sequence is moved to an output directory.

Folders are compared based on whatever the first word of their name is (gene name is this case). The first word should be followed by an underscore with more information. Below is an example of a folder name from this project:

>ACTR2_ENST00000260641.10

So, following the example name, the script will determine the average sequence length for each folder beginning with "ACTR2".

Note that **this script assumes each fasta file only has one sequence**. The average is calculated by dividing the total length of all sequences in a folder combined by the total number of files in the folder.

To use this script, edit the "rootPath", "inPath", and "outPath" variables in the main method. The rootPath should be set to the most recent common folder between the desired input and output directories. Then, the desired input and output path should be specified at inPath and outPath respectively. Each of these will use the "rootPath" variable, so only include pathing not included in the rootPath.

This script is designed for windows, but can be tweaked for unix systems (change instances of "\\\\" to "/").

### seqUnavailRemover

### transcriptCounter

This is an older script meant for counting the number of transcripts in a fasta file for each gene. The final counts of genes and transcripts can be output to a csv file for spreadsheet representation. The CSV output can either be written in a non-ordered or ordered manner (based on a desired order CSV input). The script will run assuming that fasta headers are separated by pipes (|) and that the gene name is the last piece of information in the header. See an example below:

>ENSG00000105698.16|ENST00000222305.8|USF2

To use this script, the desired methods must be called from the main method. Edit the "file" variable with the input path of the desired fasta file. From there the csvCreator or csvOrderedCreator may be called on the read in fasta file dictionary (countedGenes variable). Lastly, writeToFile may be called to output the data in csv format. Be sure to specify the output directory there.

## BASH Scripts

These scripts are either for file manipulation or program execution.