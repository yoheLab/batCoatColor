#!/bin/bash
#SBATCH --job-name=batBLAST
#SBATCH --partition=Orion
#SBATCH --time=99:00:00
#SBATCH --nodes=4
#SBATCH --mail-type=ALL
#SBATCH --mem=4G

module load blast/2.11.0+

for FILE in BlastDatabases/*DB
do
  	strippedName="${FILE#*ses/}"
        # echo "${strippedName%GCA*}DB" > testFile.txt
        # mkdir BlastDatabases/"${strippedName%GCA*}DB"
        # makeblastdb -in $FILE -title "${strippedName%_GCA*}" -dbtype nucl -out BlastDatabases/"${strippedName%GCA*}DB"/"${strippedName%GCA*}"
	# strippedName = "${FILE#*ses/}"
	tblastn -query QueryFiles/fixedFasta1to100.fasta -db $FILE/"${strippedName%DB}" -num_threads 4 -num_alignments 1000 -outfmt 6 -out BlastResults/Genes0to100/"${strippedName%_DB}.tblastn"
	# echo "${strippedName%_DB}"
done


# tblastn -query QueryFiles/demoProteinSequencesSingle.fasta -db BlastDatabases/1Demo_DB/singleDemo -num_threads 4 -num_alignments 1000 -outfmt 6 -out BlastResults/1singleDemo.tblastn
# tblastn -query QueryFiles/demoProteinSequences.fasta -db BlastDatabases/1Demo_DB/singleDemo -num_threads 4 -num_alignments 1000 -outfmt 6 -out BlastResults/MultiDemo.tblastn
