#!/bin/bash

# Reveiws a list of file names one row at a time
cat batGCAList | while read p
do

    # -f checks if the file exists, $p is the file name read in by the loop
    if [ -f ../Dino_OR_project/All_Taxa/$p ]
    	
    	# Move the file to the desired directory
    	then mv ../Dino_OR_project/All_Taxa/$p BatGenomes
    fi
done
