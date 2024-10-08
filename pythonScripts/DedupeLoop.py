import subprocess
import os

# Gets files and filters out non-fasta files, also adds full file path to each entry
def getFiles(tempFolder):
    tempFolderPath =  inputFolder + "/" + folder
    tempFolderFiles = os.listdir(tempFolderPath)
    tempFolderFiles = list(f for f in tempFolderFiles if f[len(f) - 3:len(f)] == ".fa")
    tempFolderFilePath = list(map(lambda file: inputFolder + "/" + tempFolder + "/" + file, tempFolderFiles))
    
    return tempFolderFilePath


# Takes a list of files and runs all files against each other with dedupe
def dedupe(tempFileList, outFolder):
    outputPath = outputFolder + "/" + outFolder
    formattedFiles = ""

    for f in tempFileList:
        formattedFiles = formattedFiles + f.strip() + ","
    
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    outName = (tempFileList[0].rsplit("/"))
    outName = outName[len(outName) - 1]
    outName = outName.split("_part1")
    outName = str(outName[0] + outName[1])
    outputPath += "/" + outName
    
    # os.rename(f, outputPath) use for non-deduped entries

    result = subprocess.Popen(["bash",dedupePath,"in=" + formattedFiles[0:len(formattedFiles)-1], "out=" + outputPath]) # Comment out for moving non-dedupe genes
    
    #out, err = result.communicate()
    #if result.returncode == 0:
    #    print("Dedupe worked!")
    #else:
    #    print("out : {0}".format(out))
    #    print("err : {0}".format(err))

# Organizes list of files into species defined categories, returns dictionary
def matchPartParse(tempFileList):
    tempDict = {}

    for f in tempFileList:
        splitFile = f.split(".")
        if "noName" not in f:
            speciesName = splitFile[1][splitFile[1].find("/") + 1:len(splitFile[1])]
        else:
            speciesName = splitFile[2][splitFile[2].find("/") + 1:len(splitFile[2])]
        
        if speciesName in tempDict.keys():
            tempDict.update({speciesName:tempDict[speciesName] + [f]})
        else:
            tempDict.update({speciesName:[f]})
    
    return tempDict


# File paths
dedupePath = "/mnt/c/Users/Jacob/Desktop/BBTools/BBMap_39.08/bbmap/dedupe.sh"
inputFolder = "/mnt/c/Users/Jacob/Desktop/Wormhole/Yohe_Lab/IsolatedGenes"
outputFolder = "/mnt/c/Users/Jacob/Desktop/Wormhole/Yohe_Lab/DedupeIsolatedGenes"

# Get list of gene folders
folderList = os.listdir(inputFolder)

# First loop goes through folders
for folder in folderList:
    
    # Filter out non-fasta files and organize entries by species
    # Since it is doing this within gene folders, it specifically targets match_part entries
    folderFiles = getFiles(folder)
    speciesSortedFolderFiles = matchPartParse(folderFiles)

    # If there are multiple match_part entries, checks to see if they're identical
    for x in speciesSortedFolderFiles.keys():
        if len(speciesSortedFolderFiles[x]) > 1: # Change to == 1 for moving non-dedupe genes. Keep at > 1 for dedupe genes 
            dedupe(speciesSortedFolderFiles[x], folder)

