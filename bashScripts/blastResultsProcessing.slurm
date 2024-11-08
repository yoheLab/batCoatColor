#!/bin/bash
#SBATCH --job-name=batProcessing
#SBATCH --partition=Orion
#SBATCH --time=99:00:00
#SBATCH --nodes=1
#SBATCH --mail-type=ALL
#SBATCH --mem=4G

module load bedtools2/2.29.0

# CHANGE SOURCE DIRECTORY HERE FOR PROCESSING DIFFERENT RESULTS
for FILEPATH in BlastTopHitsTranscripts/Genes*
do
	# Isolates folder name from file path, CHANGE THE TEXT IN BETWEEN STARS TO ACCAMODATE FILE PATH
	genes="${FILEPATH#*pts/*}"

	# These are for if new directories need to be made
	mkdir -p Blast2gff/"$genes"
    mkdir -p AwkOut/"$genes"
    mkdir -p BedtoolsOut/"$genes"

	for FILE in "$FILEPATH"/*.tblastn
		do
			# Variables
			fileName="${FILE#*00/*}" # Gets the filename from the path for dynamic naming
			species="${fileName%.tblastn}" # Isolates the species name from the tblastn file
			genome=BatGenomes/"${species}*.fna" # Uses isolated species to find corresponding genome assembly

			# These commands process the tblastn file into fasta fles. They can be used individually or all at once
			python blast2gff.py -b BlastTopHitsTranscripts/$genes/$fileName >Blast2gff/"$genes"/"$fileName".output.gff3
			awk -vOFS='\t' '{$3 = $9; print}' Blast2gff/"$genes"/"$fileName".output.gff3 > AwkOut/"$genes"/"$fileName".output.name
			bedtools getfasta -fi $genome -bed AwkOut/"$genes"/"$fileName".output.name -s -name -fo BedtoolsOut/"$genes"/"$fileName".fa
		done
done

# dedupe.sh in=1singleDemo.fa.out out=1singleDemo.fasta

