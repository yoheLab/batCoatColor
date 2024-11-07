#!/bin/bash
#SBATCH --job-name=batProcessing
#SBATCH --partition=Orion
#SBATCH --time=99:00:00
#SBATCH --nodes=1
#SBATCH --mail-type=ALL


# CHANGE SOURCE DIRECTORY HERE FOR PROCESSING DIFFERENT RESULTS
for blastResult in NonBatBedtoolsOut/Genes0to100/*.fa
do
	fileName="${blastResult#*00/*}" # Gets the filename from the path for dynamic naming
	cat NonBatBedtoolsOut/Genes0to100/$fileName NonBatBedtoolsOut/Genes101to200/$fileName NonBatBedtoolsOut/Genes201to300/$fileName NonBatBedtoolsOut/Genes301to400/$fileName NonBatBedtoolsOut/Genes401to500/$fileName NonBatBedtoolsOut/Genes501to600/$fileName NonBatBedtoolsOut/Genes601to700/$fileName NonBatBedtoolsOut/Genes701to800/$fileName NonBatBedtoolsOut/Genes801to900/$fileName NonBatBedtoolsOut/Genes901+/$fileName >> NonBatBlastProcessedResults/$fileName
done
