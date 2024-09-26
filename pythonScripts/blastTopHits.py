import os


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
            # Missing corresponds to any gene that had atleast one invalid entry
            elif row == "Sequence unavailable" or row == "":
                missing.append(header)
            elif row[(len(row)-1)] != "*":
                seq += row 

            # Adds the sequence into the main dictiinary based on the header   
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

def SubFinder(mainDir, subDirPrefix):
    dirList = []
    for dir in os.listdir(mainDir):
        if dir.find(subDirPrefix) != -1:
            dirList.append(dir)
    
    return dirList

def FileFinder(rootDir, subFolders, mode):
    for subFolder in subFolders:
        files = os.listdir(rootDir + "/" + subFolder)
        for file in files:
            if file.find("tblastn") != -1:
                match mode:
                    case "BlastTop":
                        BlastFindTopHit(rootDir + "/" + subFolder + "/" + file)
                    case "HeaderExchange":
                        HeaderExchange(rootDir + "/" + subFolder + "/" + file)
                    case "HeaderShift":
                        HeaderShift(rootDir + "/" + subFolder + "/" + file)

def HeaderExchange(fileName):

    with open(fileName) as fileData:
        splicedPath = fileName.split("/")
        dirCheck(splicedPath[len(splicedPath) - 2])

        # Create output file
        outputName = outputLocation + splicedPath[len(splicedPath) - 2] + "/" + splicedPath[len(splicedPath) -1]
        outputFile = open(outputName, "w")
        print(outputName)

        for line in fileData:
            splicedLine = line.split("\t")
            splicedHeader = splicedLine[0].split("|")
            for header in transcriptDict.keys():
                splicedTranscriptHeader = header.split("_")
                match len(splicedTranscriptHeader):
                    case 3:
                        check = [splicedTranscriptHeader[0][1:len(splicedTranscriptHeader[0])], splicedTranscriptHeader[2]]

                    case 4:
                        check = [splicedTranscriptHeader[0][1:len(splicedTranscriptHeader[0])], splicedTranscriptHeader[2], splicedTranscriptHeader[3]]

                    case 5:
                        check = [splicedTranscriptHeader[0][1:len(splicedTranscriptHeader[0])], splicedTranscriptHeader[2], splicedTranscriptHeader[3], splicedTranscriptHeader[4]]
                if check == splicedHeader:
                    splicedLine[0] = ">" + splicedPath[6][0:splicedPath[6].find(".")] + "." + header[1:header.rfind("_")]
                    for entry in splicedLine:
                        if entry.find("\n") == -1:
                            outputFile.write(entry + "\t")
                        else:
                            outputFile.write(entry)           

def BlastFindTopHit(fileName):
    with open(fileName) as fileData:
        
        splicedPath = fileName.split("/")
        dirCheck(splicedPath[len(splicedPath) - 2])
        
        # Create output file
        outputName = outputLocation + splicedPath[len(splicedPath) - 2] + "/" + splicedPath[len(splicedPath) -1]
        outputFile = open(outputName, "w")

        # Get the first line of the file
        bestLine = str([next(fileData) for _ in range(1)])
        bestLine = bestLine[2:len(bestLine) - 2].split("\\t")
        bestLine[len(bestLine) - 1] = bestLine[len(bestLine) - 1].replace("\\n", "\n")

        for line in fileData:
            splitLine = line.split("\t") # Name at 0, percent identity at 2, E-value at 10 
            if str(splitLine[0]) == str(bestLine[0]):
                bestLine = compareEntries(splitLine, bestLine)
            
            else:
                for entry in bestLine:
                    if entry.find("\n") == -1:
                        outputFile.write(entry + "\t")
                    else:
                        outputFile.write(entry)
                bestLine = splitLine

def HeaderShift(fileName):
    with open(fileName) as fileData:
        
        splicedPath = fileName.split("/")
        dirCheck(splicedPath[len(splicedPath) - 2])
        
        # Create output file
        outputName = outputLocation + splicedPath[len(splicedPath) - 2] + "/" + splicedPath[len(splicedPath) -1]
        outputFile = open(outputName, "w")

        counter = 0
        for line in fileData:

            splitLine = line.split("\t") # Name at 0, percent identity at 2, E-value at 10 
            splitHeader = splitLine[0].split("_")
            
            if len(splitHeader) == 4:
                newHeader = (splitHeader[0] + "_" + splitHeader[1] + "_" + splitHeader[3] + "|" + str(counter) + "_" + splitHeader[2])

            else:
                newHeader = (splitHeader[0] + "_" + splitHeader[1] + "_" + "noName|" + str(counter) + "_" + splitHeader[2])

            splitLine[0] = newHeader
            #print(splitLine)
            
            for entry in splitLine:
                if entry.find("\n") == -1:
                    outputFile.write(entry + "\t")
                else:
                    outputFile.write(entry)

            counter += 1
            #outputFile.write(entry + "\t")
            #outputFile.write

def compareEntries(newEntry, bestEntry):
    
    """
    print(float(newEntry[10]))
    print(float(bestEntry[10]))
    print(float(newEntry[10]) < float(bestEntry[10]))
    """
    if float(newEntry[10]) < float(bestEntry[10]):
        print("Wow! " + str(newEntry[10]) + " is less than " + str(bestEntry[10]))
        return newEntry
    return bestEntry

def dirCheck(dirName):
    if not os.path.exists(outputLocation + dirName):
        os.makedirs(outputLocation + dirName)





print ("Hello world!")

directoryPath = "/home/jacob/Desktop/NonBatBlastProcessedResults" # "/home/jacob/Desktop/BlastResultsPreProcess"
outputLocation = "/home/jacob/Desktop/NonBatMasterFasta/"
subFolders = "Genes"

folders = SubFinder(directoryPath, subFolders)

#FileFinder(directoryPath, folders, "HeaderShift")
#FileFinder(directoryPath, folders, "HeaderShift")

transcriptDict = fastaReader("/home/jacob/Desktop/Yohe/transcriptMasterQueryFile.fasta")

FileFinder(directoryPath, folders, "HeaderShift")

#for x in transcriptDict.keys():
#    print(x + "\n" + str(transcriptDict[x]) + "\n")

#FileFinder(directoryPath, folders, "HeaderExchange")

#FileFinder(directoryPath, folders, "BlastTop")