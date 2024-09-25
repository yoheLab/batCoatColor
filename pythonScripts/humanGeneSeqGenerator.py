import os

# Loops through the folders from the data set and checks them against the sorted queries.I
# if any folder did not get a query file, it will be printed here
def missing():
    for file in files:
        if not file in nameList:
            print(file)

# Takes a single fasta query and turns it into a file (based on header)
# realHeader is the header of the fasta query, header is the folder name found by nameCheck(), ID is the geneID
def writeFasta(realHeader, header, ID):
    
    # Genes with no common name
    if "noName" in header:
        outputFile = open(outPath + "\\" + header + "\\" + "Homo_sapien." + header + ".fa", "w")
        moreHeaderParts = realHeader.split("|")
        outputFile.write(">" + "Homo_sapien_noName_" + moreHeaderParts[0] + "_" + moreHeaderParts[1])
        outputFile.close()
    
    # Genes with a common name
    else:
        outputFile = open(outPath + "\\" + header + "\\" + "Homo_sapien." + header + ".fa", "w")
        moreHeaderParts = realHeader.split("|")
        outputFile.write(">" + "Homo_sapien_" + moreHeaderParts[2] + "_" + moreHeaderParts[0] + "_" + moreHeaderParts[1] + "\n" + fastaDict[realHeader])
        outputFile.close()

# Filters out files from a list that aren't of a specified file type
def fileFilter(fileList, fileType):
    for f in fileList:
        if f.find(fileType) == -1:
            fileList.remove(f)
    return fileList

# Reading in fasta file as dictionary
def fastaToDict(fasta):
    
    tempDict = {}

    # Loop through the file contents
    with open(fasta) as inputFileData:
        for line in inputFileData:
            
            # Header is dict key
            if line[0] == ">":
                header = line[1:].strip()
                tempDict.update({header:""})
            
            # Sequence is stored under corresponding header
            elif line.strip() != "":
                tempDict[header] += str(line.strip())
            
    return tempDict

# Checks to see if a fasta query is apart of the file list
# mockFileName uses the same system that was used to create the folder names for this data set
def nameCheck(header):
    headerParts = header.split("|")
    
    # For queries without a common gene symbol
    if len(headerParts) == 2:
        mockFileName = "noName_" + str(headerParts[0]) + "_" + str(headerParts[1])
        if mockFileName in files:
            return mockFileName, headerParts[0]
        else:
            return "!NOPE!", "!"
    
    # For queries with a common gene  symbol
    elif len(headerParts) == 3:
        mockFileName =  str(headerParts[2]) + "_" + str(headerParts[1])
        if mockFileName in files:
            return mockFileName, headerParts[0]
        else:
            return "!NOPE!", "!"

# Different file paths
humanPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\humanAllGenes.txt"
outPath =  "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\LongestDedupeIsolatedGenes"

nameList = []
files = os.listdir(outPath)

# Converts a fasta file into a dictionary
fastaDict = fastaToDict(humanPath)

for header in fastaDict.keys():
    
    # Check if a gene query is present in the data set
    name, geneID = nameCheck(header)
    
    # name[0] will be ! if no corresponding folder is found
    if not name[0] == "!":
        nameList.append(name)
        writeFasta(header, name, geneID)

# Checks to see if folders from the data set did not get a corresponding query
missing()
