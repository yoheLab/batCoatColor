#!/bin/bash
#SBATCH --job-name=batProcessing
#SBATCH --partition=Orion
#SBATCH --time=99:00:00
#SBATCH --nodes=4
#SBATCH --mail-type=ALL
#SBATCH --mem=4G


# CHANGE SOURCE DIRECTORY HERE FOR PROCESSING DIFFERENT RESULTS
for blastResult in NonBatBedtoolsOut/Genes0to100/*.fa
do
	# Isolates folder name from file path
	# genes="${FILEPATH#*lts/*}"

	# These are for if new directories need to be made
	# mkdir -p Blast2gff/"$genes"
        # mkdir -p AwkOut/"$genes"
        # mkdir -p BedtoolsOut/"$genes"

	#echo "$FILE GIMME A HIGHER LOVE \n"
	# Variables 
	fileName="${blastResult#*00/*}" # Gets the filename from the path for dynamic naming
	echo $blastResult
	echo $fileName
	cat NonBatBedtoolsOut/Genes0to100/$fileName NonBatBedtoolsOut/Genes101to200/$fileName NonBatBedtoolsOut/Genes201to300/$fileName NonBatBedtoolsOut/Genes301to400/$fileName NonBatBedtoolsOut/Genes401to500/$fileName NonBatBedtoolsOut/Genes501to600/$fileName NonBatBedtoolsOut/Genes601to700/$fileName NonBatBedtoolsOut/Genes701to800/$fileName NonBatBedtoolsOut/Genes801to900/$fileName NonBatBedtoolsOut/Genes901+/$fileName >> NonBatBlastProcessedResults/$fileName
done
