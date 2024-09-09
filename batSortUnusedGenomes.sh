#!/bin/bash

# Reveiws a list of file names one row at a time
cat batFileNameUnuseList | while read p
do

    # -f checks if the file exists, $p is the file name read in by the loop
    if [ -f BatGenomes/$p ]
    	
    	# Move the file to the desired directory
    	then mv BatGenomes/$p BatGenomes/UnusedBatGenomes
    fi
done
