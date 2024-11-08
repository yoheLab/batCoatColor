#!/bin/bash
#SBATCH --job-name=batBLAST
#SBATCH --partition=Orion
#SBATCH --time=99:00:00
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=16
#SBATCH --mail-type=ALL
#SBATCH --mem=4G

module load blast/2.11.0+

for FILE in BlastDatabases/*DB
do
  	strippedName="${FILE#*ses/}"
    # echo "${strippedName%GCA*}DB" > testFile.txt
	tblastn -query QueryFiles/fixedFasta1to100.fasta -db $FILE/"${strippedName%DB}" -num_threads 64 -num_alignments 1000 -outfmt 6 -out BlastResults/Genes0to100/"${strippedName%_DB}.tblastn"
done
