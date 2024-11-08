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

This is another multipurpose script that does a few miscellaneous things in the realm fasta parsing. Using the fastaReader method, one may read in a fasta file as a dictionary. These dictionaries may be input into a few different methods. The fasta reader method also has an option to note the headers that are missing a fasta sequence.

This script has two methods for writing an output fasta file, fastaWriterTrack and fastaWriterStandard. fastaWriterStandard will output a fasta file with the dictionary key as a fasta header. The track variant of this method does the same thing but adding a number to each entry where the gene ID and gene name are the same. This effectively identifies different transcripts of the same gene using a number. Though I would advise not using fastaWriterTrack and just using a transcript ID instead.

transcriptCounterOrdered counts the number of transcripts found for each gene ID based upon the input dictionary. These results are then output as a table. This variant of the method does this in a particular order, specified by the order of the list entered into the th method. 

checkMissing determines if any genes are missing from a fasta dictionary based upon an input file. It will print the gene ID of any gene it cannot find to the console. 

Shortest seq calc will determine which sequence in a dictionary is the  shortest and it will print that result to the console. It will also say how long said sequence is.

the final method is matchTranscript, which has a fairly niche use case. This method was used to correct the headers of a fasta dictionary. The original headers had extra numbers as they were written using fastaWriterTrack. These numbers became problematic later down the pipeline, so they needed to be replaced with transcript IDs. So, this method was written to take two dictionaries, one corresponding to the messed up fasta file, and the other to a new fasta file with proper headers. The sequences are matched based on sequence, and the headers are replaced. One might wonder why the new fasta was not just used. This is because some processing steps and data generation had already been done on the old fasta file, thus it would have been preferred to keep the old file while fixing the headers.

### transcriptCounter

This is an older script meant for counting the number of transcripts in a fasta file for each gene. The final counts of genes and transcripts can be output to a csv file for spreadsheet representation. The CSV output can either be written in a non-ordered or ordered manner (based on a desired order CSV input). The script will run assuming that fasta headers are separated by pipes (|) and that the gene name is the last piece of information in the header. See an example below:

>ENSG00000105698.16|ENST00000222305.8|USF2

To use this script, the desired methods must be called from the main method. Edit the "file" variable with the input path of the desired fasta file. From there the csvCreator or csvOrderedCreator may be called on the read in fasta file dictionary (countedGenes variable). Lastly, writeToFile may be called to output the data in csv format. Be sure to specify the output directory there.

## BASH Scripts

These scripts are either for file manipulation or program execution on the HPC.

### batListNew

Functionality very similar to batSortUnusedGenomes. See that section for more information.

### batSort

Functionality very similar to batSortUnusedGenomes. See that section for more information.

### batSortUnusedGenomes

This script was used to move undesired genomes from one directory to another. It does so using a for loop on a list of file names. These file names correspond to the genomes that should be moved to a different directory. The script then checks to see if that file exists in the directory specified and moves it if it does. 

If one wishes to use this script, they should create a list of filenames that they wish to move. The filename of that list should be specific in the cat command right before the while loop. Entries from the file will be read into the loop under the variable named $p

The if statement is used to check if a given file exists. One should edit the file path to correspond to the desired directory while keeping $p at the end. The -f flag is what checks if the file exists. 

In the then mv command, one should ensure that the first file path is identical to the one specified in the if statement. The second file path should correspond to the desired output directory.

### blastGenes100

This script was used to execute blast. Particularly, this script uses one blast query and blasts each database in a specified directory. 

The header for this script is important. The "#SBATCH --nodes==4" will determine how quickly blast will execute. More nodes will increase speed, but make it more difficult for the job to begin (you will need to wait for nodes to become free). However, if this line is changed, one part of the tblastn query will also need to be changed. The -num_threads flag specifies the number of threads that the blast job will utilize. Given that (at the time of writing) each node consists of 16 CPUs (see https://oneit.charlotte.edu/urc/research-clusters/orion-gpu-slurm-user-notes/), the number following the -num_threads flag should be 16 times the number of nodes specified. In this case, 4 nodes are requested, so 64 threads are specified. If blast cannot find this many threads, it will automatically default to the maximum number it can use with the nodes it is given. It should also be noted that "#SBATCH --ntasks-per-node=16" also denotes the number of CPUs to be used per node.

The for loop will loop through every database it finds in the specified directory. See databaseGenerator for more information on blast database creation. This file path may be changed to suit one's needs.

The strippedName variable is set to isolate the file name from the file path. This is done for dynamic file naming after utilizing the blast command but also for the -db flag in the tblastn command. One should change the the text in between "FILE#*" and "/}" to the name of the folder that the data base folders are located in.

The tblastn command will take a query of fasta files and find regions of similarity in data base files. It has multiple flags that may be used to fine tune this process. the -query flag is for specifying the blast query. the -db flag is for specifying the blast database files. Due to the fact that a blast database consists of multiple files, each organism was given it's own database folder. For this reason, both the organism folder ($FILE) and the organism name ("${strippedName%DB}") must be provided as a file path. num_threads specifies the number of CPUs or threads that the blast job will use. -num_alignments specifies the number of alignments to be shown in the output files. I think this is per query, not corresponding to a file of multiple queries. -outfmt specifies the output format that blast will write it's results to. Most cases I have seen use outfmt 6, and this projects processing script also relies on using said format. One may look up what the columns of this output format correspond to. Finally, the -out flag specifies an output directory. In this case, ${strippedName%_DB} is used for dynamic file naming.

### blastResultsProcessing

This script is for processing blast results. The goal of this script is to execute the blast2gff python script, the awk command, and the bedtools getfasta command on every tblastn file to convert it into a fasta file. This particular version operates under a file structure that looks as follows:

>- BaseFolder
>   - FirstGeneQueryFolder
>       - speciesOne.tblastn
>       - speciesTwo.tblastn
>       - speciesThree.tblastn
>   - SecondGeneQueryFolder  
>       - speciesOne.tblastn
>       - speciesTwo.tblastn
>       - speciesThree.tblastn

The first loop of the script goes through each gene query folder. The second loop goes through each species for said folders. 

An alternative to this loop structure would be to concatenate the results together. Concatenation would likely be more efficient in most instances.

Within the second loop is where the processing commands are located. prior to the processing commands, some variables are set up. fileName isolates an individual filename from a filepath. Change the text in between FILE# and /* to the name of the folder blast result files are located in. species uses this variable to isolate the species name. This variable is only used to create the final variable, being the genome assembly variable. The genome assembly variable update dynamically based upon the file being processed. This is done for the final command (bedtools getfasta).

Following the variable are the processing commands. These were based upon a script shown to me by Dr. Yohe, so I am not entirely sure on the specifics of all of them. If one wishes yo use them, just change the input and output locations for each command. python blast2gff.py uses -b for input and > for output. awk has it's input directory directly before the > and it's output directory directly after. For the bedtools getfasta command, the input directory is specified following -bed and the output directory is specifiedd at the end following -fo. Know that for this command, a genome assembly also needs to be provided after the -fi command. 

### concatenateResults

This script was used to concatenate multiple files (blast results in particular) across multiple folders into one file. This project initially broke it's blast run's into multiple runs (10 blast queries of ~100 genes each), so this script was used to combine results.

The script gets a file name (corresponding to one species) from one folder, then concatenates all files corresponding to that species together and outputs it to a different folder. 

To use this script, alter the file path in the for loop to correspond to one of the folders. If concatenating fasta files, keep the *.fa at the end of the file path. 

The fileName variable isolates specific file names from a whole file path. Change the text in between "blastResult#* and "/*" to correspond to the folder name that files are located in. The cat command should be changed to include each file path that is desired. One may add/remove as many file paths as desired. Ensure to include $fileName at the end of each file path, as that corresponds directly to file names.

The output location is specified after the >>. It is recommended that the filepath include $fileName at the end to avoid conflict in file creation. Outside of that, any directory may be specified. 

### dataBaseGenerator

This script is for creating multiple database files from a folder of genome assemblies (or .fna files)

Database files are used by blast, serving as the subject sequence to search for queries on. 

To use this script, first change the file path in the for loop to where ever the desired genomes assemblies are located. Keep the *fna* in the file path, as that is what filters out non-genome assembly files. Genome assembly files for this project followed the following example name:

> Aeorestes_cinereus_GCA_011751065.1_genomic.fna.gz

The strippedName variable may also need to be altered. It isolated the file name from the file path. To use this variable, alter the text following "FILE#*". This should correspond to the folder name that the genome files are located in.

In the makeblastdb command, the loop variable ($FILE) is used to select an input file. The output location corresponds to a folder or subfolders containing database info on a per species basis. ${"strippedName%GCA*} corresponds to the species name.

