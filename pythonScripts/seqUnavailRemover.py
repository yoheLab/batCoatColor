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

def fastaWriterTrack(inputDict, outputFileName):
    
    # Name of output file
    outputFile = open(outputFileName, "w")

    # Loop for going through the list under each key and putting it into fasta format
    for key in inputDict.keys():
        if inputDict[key] != []:

            # Transcript number tracks the number of transcripts each gene has (header in dict)
            transcriptNumber = 0

            # Loops through lists under each header
            for value in inputDict[key]:
                
                # If applicable, marks fasta entries at a designated frequency (every 100th entry, every 150th entry, etc)
                outputFile.write(key + "|"+ str(transcriptNumber) + "\n" + value + "\n\n")
                
                # Adds 1 to tracking variables
                transcriptNumber += 1
        
        # This will point out any sequences that do not end in a stop codon
        else:
            print("Check - " + key)

def fastaWriterStandard(inputDict, outputFileName):
        
    # Name of output file
    outputFile = open(outputFileName, "w")

    # Loop for going through the list under each key and putting it into fasta format
    for key in inputDict.keys():
        if inputDict[key] != []:

            if type(inputDict[key]) == list:
            # Loops through lists under each header
                for value in inputDict[key]:
                    outputFile.write(key + "\n" + value + "\n\n")

            elif type(inputDict[key]) == str:
                outputFile.write(key + "\n" + inputDict[key] + "\n\n")

        # This will point out any sequences that do not end in a stop codon
        else:
            print("Check - " + key)

def transcriptCounterOrdered (inputDict, geneListInput, outputFileName):
    
    # Variables for ordering 
    idString = ""
    numberString = ""

    # Opens gene list, meant for determining the order genes are placed in
    with open(geneListInput) as fileData:
        transcriptList = str(list(fileData))
        transcriptList = transcriptList[2:len(transcriptList) - 4]
        transcriptList = transcriptList.split(",")
        
        # Loops through gene's as a list
        for x in transcriptList:
        
            # Loops through headers in the input dictionary and checks where they are in the list
            for key in inputDict.keys():
                if x in key:
                    idString += x + ","
                    numberString += (str(len(inputDict[key])) + ",")
            if x not in idString:
                idString += x + ","
                numberString += (str(0) + ",")
        
        # Output file
        transcriptFile = open(outputFileName, "w")
        transcriptFile.write(idString + "\n" + numberString)

def checkMissing(inputDict, geneListInput):
    
    # Opens and formats gene list to check input dict against
    with open(geneListInput) as fileData:
        transcriptList = str(list(fileData))
        transcriptList = transcriptList[2:len(transcriptList) - 4]
        transcriptList = transcriptList.split(",")
        
        # Loops through input dict keys and checks iff they are in the transcript list file
        for key in inputDict.keys():
            id = key[1: key.find(".")]            
            
            # If a gene is not listed, this prints
            if id not in transcriptList:
                print("Missing gene - " + id)

def shortestSequenceCalc(inputDict):
    
    # Creates list of keys and initially defines the shortest entry as the first dictionary result
    cool = list(inputDict.keys())
    shortestEntry = str(inputDict[cool[0]])
    
    # For loop goes through dictionary keys
    for entry in cool:
        
        # For loop goes through each entry for those keys 
        # This is important as entries are in a list format
        for realEntry in inputDict[entry]:
            
            # Checks if the current entry is shorter than the previous ones
            if len(realEntry) < len(shortestEntry):
                shortestEntry = str(realEntry)

    # Print results (change to return if necessary)
    print(shortestEntry + "\n" + str(len(shortestEntry)))

def matchTranscript(originalDict, transcriptDict):
    newDict = {}
    for oKey in originalDict.keys():

        for tKey in transcriptDict.keys():
            if transcriptDict[tKey] == originalDict[oKey]:
                splicedTKey = tKey.split("|")
                splicedOKey = oKey.split("|")
                if len(splicedOKey) == 2:
                    newHeader = str(splicedTKey[0] + "_" + splicedTKey[1] + "_" + splicedOKey[1])
                elif len(splicedOKey) == 3:
                    newHeader = str(splicedTKey[0] + "_" + splicedTKey[1] + "_" + splicedOKey[1] + "_" + splicedOKey[2])
                else:
                    newHeader = str(splicedTKey[0] + "_" + splicedTKey[1] + "_" + splicedOKey[1] + "_" + splicedOKey[2] + "_" + splicedOKey[3])
                newDict.update({newHeader:str(transcriptDict[tKey])[2:len(str(transcriptDict[tKey])) - 2]})
                break
    return newDict

originalQuery = fastaReader("fixedFastaMaster.fasta")
transcriptQuery = fastaReader("transcriptIDs.fasta")

fixedDict = matchTranscript(originalQuery, transcriptQuery)

fastaWriterStandard(fixedDict, "transcriptMasterQueryFile.fasta")


#for x in fixedDict.keys():
#    print(x + "\n" + str(fixedDict[x]) + "\n")


#zamnDict = fastaReader("fixedFastaMaster.fasta")

#shortestSequenceCalc(zamnDict)

"""
newDict, missing = fastaReader("toyFasta.fasta", True)

fastaWriter(newDict, "toyFastaTesting")

transcriptCounterOrdered(newDict, "TranscriptOrder.csv" , "toyFastaCountsTesting.csv")

checkMissing(newDict, "TranscriptOrder.csv")

print(len(newDict))
print(missing)
"""