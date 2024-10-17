import os

# Read in a fasta file and return a dictionary (key is fasta header and value is fasta sequence)
# Using countMisssing will also create a list of headers that have at least one missing/messed up entry
def fastaReader(fileName, countMissing=False):
    
    # Variables
    missing = []
    seq = ""
    header = ""
    tempDict = {}

    # Open the file
    with open(fileName) as fileData:
        
        # Loop reads in data one row a time
        for row in fileData:
            row = str(row.strip())

            # If statement finds headers and adds them to the dictionary
            if row.startswith(">"):
                header=row
                if header not in tempDict.keys():
                    tempDict.update({header:[]})
                seq = ""
            
            # Rows following the header are part of the sequence, they are added to the header key
            # Missing corresponds to any gene that had at least one invalid entry
            elif row == "Sequence unavailable" or row == "":
                missing.append(header)
            elif row[(len(row)-1)] != "*":
                seq += row 

            # Adds the sequence into the main dictionary based on the header   
            else:
                seq += row
                newList = tempDict[header]
                newList.append(seq)
                tempDict.update({header:newList})
                
    
    # Return the constructed dictionary and heading of missing sequences (if applicable)
    if countMissing == True:
        return tempDict, missing
    else:
        return tempDict

# Will return a list of folder names from within a specified directory based on a common folder prefix
def SubFinder(mainDir, subDirPrefix):
    dirList = []
    for dir in os.listdir(mainDir):
        if dir.find(subDirPrefix) != -1: # Eliminates folders or files without the prefix
            dirList.append(dir)
    
    return dirList

# Loops through each folder and subfolder to find tblastn files. Each file has a method invoked on it
def FileFinder(rootDir, subFolders, mode):
    for subFolder in subFolders:
        files = os.listdir(rootDir + "/" + subFolder)
        for file in files:
            if file.find("tblastn") != -1: # Ignores any non tblastn files
                match mode:
                    case "BlastTop":
                        BlastFindTopHit(rootDir + "/" + subFolder + "/" + file)
                    case "HeaderExchange":
                        HeaderExchange(rootDir + "/" + subFolder + "/" + file)
                    case "HeaderShift":
                        HeaderShift(rootDir + "/" + subFolder + "/" + file)

# This method will attempt matching items from the transcript dictionary with fasta header column of the entered file
def HeaderExchange(fileName):

    with open(fileName) as fileData:
        splicedPath = fileName.split("/")

        # Create output file
        dirCheck(splicedPath[len(splicedPath) - 2])
        outputName = outputLocation + splicedPath[len(splicedPath) - 2] + "/" + splicedPath[len(splicedPath) -1]
        outputFile = open(outputName, "w")

        for line in fileData:
            splicedLine = line.split("\t")
            splicedHeader = splicedLine[0].split("|")
            
            # Loop compares every header against the current line
            for header in transcriptDict.keys():
                splicedTranscriptHeader = header.split("_")
                
                # Format transcript header to look like tblastn header
                match len(splicedTranscriptHeader):
                    case 3:
                        check = [splicedTranscriptHeader[0][1:len(splicedTranscriptHeader[0])], splicedTranscriptHeader[2]]

                    case 4:
                        check = [splicedTranscriptHeader[0][1:len(splicedTranscriptHeader[0])], splicedTranscriptHeader[2], splicedTranscriptHeader[3]]

                    case 5:
                        check = [splicedTranscriptHeader[0][1:len(splicedTranscriptHeader[0])], splicedTranscriptHeader[2], splicedTranscriptHeader[3], splicedTranscriptHeader[4]]
                
                # If the transcript header matches the current blast header, the current blast header is replaced
                if check == splicedHeader:
                    splicedLine[0] = ">" + splicedPath[6][0:splicedPath[6].find(".")] + "." + header[1:header.rfind("_")] # splicedPath reference gets species name
                    for entry in splicedLine:
                        if entry.find("\n") == -1:
                            outputFile.write(entry + "\t")
                        else:
                            outputFile.write(entry)           

# Loops through each blast entry in a file and compares hits with the same header against each other to find the best one
def BlastFindTopHit(fileName):
    with open(fileName) as fileData:
        
        splicedPath = fileName.split("/")
        
        # Create output file
        dirCheck(splicedPath[len(splicedPath) - 2])
        outputName = outputLocation + splicedPath[len(splicedPath) - 2] + "/" + splicedPath[len(splicedPath) -1]
        outputFile = open(outputName, "w")

        # Get the first line of the file
        bestLine = str([next(fileData) for _ in range(1)])
        bestLine = bestLine[2:len(bestLine) - 2].split("\\t")
        bestLine[len(bestLine) - 1] = bestLine[len(bestLine) - 1].replace("\\n", "\n")

        # Loop through the rest of the lines in a file
        for line in fileData:
            splitLine = line.split("\t") # Name at 0, percent identity at 2, E-value at 10 
            
            # Comparison takes place
            if str(splitLine[0]) == str(bestLine[0]):
                bestLine = compareEntries(splitLine, bestLine)
            
            # All entries of the header have been checked, so the best is written to the output file
            else:
                for entry in bestLine:
                    if entry.find("\n") == -1:
                        outputFile.write(entry + "\t")
                    else:
                        outputFile.write(entry)
                
                # New entry is checked
                bestLine = splitLine

# Used for cleaning up fasta headers in the first column of a tblastn output file (outfmt 6)
# There is a counter used to differentiate hits with the same characteristics from each other. This is inefficient for data analysis so it is recommended that a different script from the repo be used
def HeaderShift(fileName):
    with open(fileName) as fileData:
        
        counter = 0
        splicedPath = fileName.split("/")
        
        # Create output file
        dirCheck(splicedPath[len(splicedPath) - 2])
        outputName = outputLocation + splicedPath[len(splicedPath) - 2] + "/" + splicedPath[len(splicedPath) -1]
        outputFile = open(outputName, "w")

        for line in fileData:

            splitLine = line.split("\t") # Name at 0, percent identity at 2, E-value at 10 
            splitHeader = splitLine[0].split("_")
            
            # Header assembly logic
            if len(splitHeader) == 4:
                newHeader = (splitHeader[0] + "_" + splitHeader[1] + "_" + splitHeader[3] + "|" + str(counter) + "_" + splitHeader[2])

            else: # Header without common gene name
                newHeader = (splitHeader[0] + "_" + splitHeader[1] + "_" + "noName|" + str(counter) + "_" + splitHeader[2])

            splitLine[0] = newHeader
            
            # Write line to output
            for entry in splitLine:
                if entry.find("\n") == -1:
                    outputFile.write(entry + "\t")
                else:
                    outputFile.write(entry)

            counter += 1

# Compares blast lines to see which one has a smaller e-value
def compareEntries(newEntry, bestEntry):
    if float(newEntry[10]) < float(bestEntry[10]):
        return newEntry
    return bestEntry

# Used for checking if a folder exists and creating a folder if it does not
def dirCheck(dirName):
    if not os.path.exists(outputLocation + dirName):
        os.makedirs(outputLocation + dirName)



# File paths
directoryPath = "/home/jacob/Desktop/NonBatBlastProcessedResults" # "/home/jacob/Desktop/BlastResultsPreProcess"
outputLocation = "/home/jacob/Desktop/NonBatMasterFasta/"
transcriptDict = fastaReader("/home/jacob/Desktop/Yohe/transcriptMasterQueryFile.fasta")

# If necessary, change to a common term present for each subfolder
subFolders = "Genes"

# List of specific sub folders
folders = SubFinder(directoryPath, subFolders)

# Use file finder if usage of sub folders is necessary, otherwise a for loop of directories should suffice
FileFinder(directoryPath, folders, "HeaderShift")
#FileFinder(directoryPath, folders, "HeaderExchange")
#FileFinder(directoryPath, folders, "BlastTop")