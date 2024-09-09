print("Hello World!")

import os

# Moves folder based on specified name. Uses predefined input/output paths 
def moveFolders(folderName):
    originalName = inPath + "\\" + folderName
    newName = outPath + "\\" + folderName
    os.rename(originalName, newName)

# Categorizes folders by gene name in a dictionary. This is useful for comparing transcripts
# Returns the dictionary it creates
def categorizeFolders(folderList):
    tempDict = {}
    for folder in folderList:
        splicedFolder = folder.split("_")
        geneName = splicedFolder[0]
        if geneName in tempDict.keys():
            tempDict[geneName].append(folder)
        else:
            tempDict.update({geneName:[folder]})
    return tempDict

# Takes a list of folder names and determines which folder has the longest gene sequences. It does this by determining the average sequence length of the files in each folder
# Returns the name of the folder with the longest gene sequences
def findLongest(folderList):
    lengthsDict = {}
    for folder in folderList:
        filePath = inPath + "\\" + folder
        fileList = os.listdir(filePath)
        lengthsDict.update({folder:0})
        for file in fileList:    
            seq = ""
            with open(filePath + "\\" + file) as fileData:
                for line in fileData:
                    if line[0] == ">":
                        pass
                    else:
                        seq += str(line)
            lengthsDict[folder] += len(seq)
        lengthsDict[folder] = lengthsDict[folder] / len(fileList)
    
    theOne = ""
    bigLength = 0

    for entry in lengthsDict:
        if lengthsDict[entry] > bigLength:
            theOne = entry
            bigLength = lengthsDict[entry]
    return(theOne)


# File paths
rootPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab"
inPath = rootPath + "\\DedupeIsolatedGenes"
outPath = rootPath + "\\LongestDedupeIsolatedGenes"

# Read folders and categorize them
folders = os.listdir(inPath)
folderDict = categorizeFolders(folders)

# Determines the folder with the longest gene sequences and adds them to a list
longestList = []
for gene in folderDict.keys():
    if len(folderDict[gene]) == 1:
        longestList.append(str(folderDict[gene])[2:len(str(folderDict[gene])) - 2])
        print(folderDict[gene])
    else:
        longestList.append(findLongest(folderDict[gene]))

# Moves the folders specified in the list on longest seq folders
for folder in longestList:
    moveFolders(folder)

