import os

def addSpecies(filePath):
    isolatedFileName = filePath[filePath.rfind("\\") + 1:len(filePath)]

    # Gets species name from file name
    speciesName = isolatedFileName[0:(isolatedFileName.find(".tb"))]

    with open(filePath) as fileContent:
        
        outputName = isolatedFileName[0:isolatedFileName.find(".") + 1] + isolatedFileName[isolatedFileName.find("tblastn."):len(isolatedFileName)]        
        outputFile = open(outPath + outputName, "w")

        for line in fileContent:
            if line[0] == ">":
                newLine = line[0:4] + ">" + speciesName + "." + line[4:]
                outputFile.write(newLine)
            else:
                outputFile.write(line)


# Specify input directory path
filePath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\BlastE50\\NewBedtoolsOut\\"

# Get all files in the input directory
fileList = os.listdir(filePath)

# Goes one file above the input directory for creating an output directory
rootPath = filePath[0:filePath.rfind("\\")]

for f in fileList:
    if f.find(".fa") == -1:
        fileList.remove(f)

# If the output directory file is not already there, create one
if not os.path.exists(rootPath + "WithSpecies"):
    os.makedirs(rootPath + "WithSpecies")

outPath = rootPath + "WithSpecies\\"


for f in fileList:
    addSpecies(filePath + f)