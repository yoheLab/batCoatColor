#!/bin/bash

# Reveiws a list of file names one row at a time
cat toBeDownloaded.txt | while read p
do

    # -f checks if the file exists, $p is the file name read in by the loop
    if [ -f BatGenomes/*$p* ]

    	# Move the file to the desired directory
    	then 
		find BatGenomes -name  *$p* >> newDownloadedGenomes.txt

    fi
done
