import os

# Generates a file name made up of species, gene name, and gene ID
def generateName(fileName, geneName, geneID, transID, partID):
    return fileName[0:fileName.find(".") + 1] + geneName + "_" + partID + "_" + geneID + "_" + transID + ".fa"

# Checks if a directory has already been created, and creates one if it hasn't
def dirCheck(dirName):
    if not os.path.exists(outPath + dirName):
        os.makedirs(outPath + dirName)

# Filters out files from a list that aren't of a specified file type
def fileFilter(fileList, fileType):
    for f in fileList:
        if f.find(fileType) == -1:
            fileList.remove(f)
    return fileList

# Goes through fasta files and splits them apart into individual files
def geneIsolation(fileList):
    
    # Loop goes through species files
    for fileName in fileList:
        with open(inputPath + fileName, "r") as fileContent:
            
            # Goes through species file line by line
            for line in fileContent:
                
                # If the line is a header
                if line[0] == ">":
                    
                    # Isolate gene name and ID
                    splicedLine = line.split("_")
                    if len(splicedLine) == 6:
                        geneName = splicedLine[2]
                        partID = splicedLine[3]
                        geneID = splicedLine[4]
                        transID = splicedLine[5].strip()
                    if len(splicedLine) == 7:
                        geneName = splicedLine[3]
                        partID = splicedLine[4]
                        geneID = splicedLine[5]
                        transID = splicedLine[6].strip()

                    dirName = geneName + "_" + transID                    
                    
                    # Set up directory and file name
                    dirCheck(dirName)
                    outputName = generateName(fileName, geneName, geneID, transID, partID)

                    # Open output file and write header
                    outputFile = open(outPath + dirName + "\\" + outputName, "w")
                    outputFile.write(line)
                
                # If the line is a sequence
                elif line != "\n":
                    
                    # Write the sequence and close the file
                    outputFile.write(line)
                    outputFile.close()

# Different file paths
rootPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab"
inputPath = rootPath + "\\NonBatMasterFasta\\" # RenamedBlastFiles
outPath = rootPath + "\\IsolatedGenes\\"

# Gets file list and filters out non-fasta files from specified directory
files = os.listdir(inputPath)
files = fileFilter(files, ".fa")

# Uses file list to create a folder for every gene and breaks down fasta files
geneIsolation(files)