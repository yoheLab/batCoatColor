#!/bin/bash
#SBATCH --job-name=batBLAST
#SBATCH --partition=Orion
#SBATCH --time=1:00:00

module load blast/2.11.0+

for FILE in NonBatGenomes/*fna*
do
	strippedName="${FILE#*mes/}"
	# echo "${strippedName%GCA*}DB" > testFile.txt
	mkdir BlastDatabases/"${strippedName%GCA*}DB"
	makeblastdb -in $FILE -title "${strippedName%_GCA*}" -dbtype nucl -out BlastDatabases/"${strippedName%GCA*}DB"/"${strippedName%GCA*}"

done