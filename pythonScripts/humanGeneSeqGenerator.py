import os

print("Hello world")

def missing():
    for file in files:
        if not file in nameList:
            print(file)

def writeFasta(realHeader, header, ID):
    if "noName" in header:
        outputFile = open(outPath + "\\" + header + "\\" + "Homo_sapien." + header + ".fa", "w")
        moreHeaderParts = realHeader.split("|")
        outputFile.write(">" + "Homo_sapien_noName_" + moreHeaderParts[0] + "_" + moreHeaderParts[1])
        outputFile.close()
    else:
        outputFile = open(outPath + "\\" + header + "\\" + "Homo_sapien." + header + ".fa", "w")
        moreHeaderParts = realHeader.split("|")
        outputFile.write(">" + "Homo_sapien_" + moreHeaderParts[2] + "_" + moreHeaderParts[0] + "_" + moreHeaderParts[1] + "\n" + fastaDict[realHeader])
        outputFile.close()

    #outputFile.write(line)

# Filters out files from a list that aren't of a specified file type
def fileFilter(fileList, fileType):
    for f in fileList:
        if f.find(fileType) == -1:
            fileList.remove(f)
    return fileList

def fastaToDict(fasta):
        
    tempDict = {}
    with open(fasta) as inputFileData:
        for line in inputFileData:
            if line[0] == ">":
                header = line[1:].strip()
                tempDict.update({header:""})
            elif line.strip() != "":
                tempDict[header] += str(line.strip())
            
    return tempDict

def nameCheck(header):
    headerParts = header.split("|")
    if len(headerParts) == 2: # for noName
        mockFileName = "noName_" + str(headerParts[0]) + "_" + str(headerParts[1])
        print(mockFileName)
        if mockFileName in files:
            return mockFileName, headerParts[0]
        else:
            return "!NOPE!", "!"
    elif len(headerParts) == 3: # for normal
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
#files = fileFilter(files, ".fa")

fastaDict = fastaToDict(humanPath)

for header in fastaDict.keys():
    
    name, geneID = nameCheck(header)
    
    if not name[0] == "!":
        nameList.append(name)
        writeFasta(header, name, geneID)

        
missing()
