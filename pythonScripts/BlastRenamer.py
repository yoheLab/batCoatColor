import os

print("Hello World!")

# Reads in a blast fasta output and converts it's blast headers
def blastRenamerOld(fileName):
    
    # Gets species name from file name
    speciesName = fileName[0:(fileName.find(".tb"))]

    # Open input file
    with open(fileName, "r") as fileContent:
        
        # Create output file name from input file name
        outputName = fileName[0:fileName.find(".") + 1] + "newname." + fileName[fileName.find("tblastn."):len(fileName)]
        
        # Attatch output file name to output file path and open the file
        outputFile = open(outPath + outputName, "w")

        # Go through file line by line
        for line in fileContent:
            
            # Begins/resets gene header with the species name
            geneHeader = ">" + speciesName + "."
            
            # If the line is a header
            if str(line)[0] == ">":
                
                # Isolates the ID and gene name
                tempParse = str(line)[line.find("t=") + 2:len(line)]
                almostGeneName = tempParse[tempParse.find(".") + 1:len(tempParse)]
                
                # For loop find the beginning of the gene name from the ID
                for char in almostGeneName:
                    if char.isnumeric() == False:
                        coolChar = char
                        break
                
                # Puts it all together
                geneName = almostGeneName[almostGeneName.find(coolChar):len(almostGeneName)]
                ensemblID = tempParse[0:tempParse.find(geneName)]
                geneHeader += geneName.strip() + "|" + ensemblID

                # Write final header to file
                outputFile.write(geneHeader + "\n")

            else:

                # Write the sequence info underneath the file
                outputFile.write(line + "\n")
    
    # Close output file
    outputFile.close()

# Reads in a blast fasta output and converts it's blast headers
def blastRenamer(fileName):
    
    isolatedFileName = fileName[fileName.rfind("\\") + 1:len(fileName)]

    # Gets species name from file name
    speciesName = isolatedFileName[0:(isolatedFileName.find(".tb"))]

    # Open input file
    with open(fileName, "r") as fileContent:
        
        # Create output file name from input file name
        outputName = isolatedFileName[0:isolatedFileName.find(".") + 1] + "newname." + isolatedFileName[isolatedFileName.find("tblastn."):len(isolatedFileName)]
        
        # Attatch output file name to output file path and open the file
        outputFile = open("G:\Other computers\My Computer\WormHole\Yohe_Lab\BlastResultsRenaming" + outputName, "w")
        print(outPath + outputName)

        # Go through file line by line
        for line in fileContent:
            
            # Begins/resets gene header with the species name
            geneHeader = ">" + speciesName + "."
            
            # If the line is a header
            if str(line)[0] == ">":
                
                # Isolates the ID and gene name
                firstParse = line.split(";")
                secondParse = firstParse[0].split("_")
                
                if speciesName.count("_") == 1:
                    if len(secondParse) == 5:
                        geneName = ">" + speciesName + "_" + secondParse[3][0:secondParse[3].find(".")] + "_" + secondParse[4] + "_" + secondParse[1][secondParse[1].find(".") + 1:len(secondParse[1])] + "_" + secondParse[2]
                    elif len(secondParse) == 4:
                        geneName = ">" + speciesName + "_noName_" + secondParse[3] + "_" + secondParse[1][secondParse[1].find(".") + 1:len(secondParse[1])] + "_" + secondParse[2][0:secondParse[2].rfind(".")]
                    else:
                        geneName = ">" + speciesName + "_" + secondParse[3] + "-" + secondParse[4][0] + "_" + secondParse[4] + "_" + secondParse[1][secondParse[1].find(".") + 1:len(secondParse[1])] + "_" + secondParse[2]

                else:
                    if len(secondParse) == 6:
                        geneName = ">" + speciesName + "_" + secondParse[4][0:secondParse[4].find(".")] + "_" + secondParse[5] + "_" + secondParse[2][secondParse[2].find(".") + 1:len(secondParse[2])] + "_" + secondParse[3]
                    elif len(secondParse) == 5:
                        geneName = ">" + speciesName + "_noName_" + secondParse[4] + "_" + secondParse[2][secondParse[2].find(".") + 1:len(secondParse[2])] + "_" + secondParse[3][0:secondParse[3].rfind(".")]
                    else:
                        geneName = ">" + speciesName + "_" + secondParse[4] + "-" + secondParse[5][0] + "_" + secondParse[6] + "_" + secondParse[2][secondParse[2].find(".") + 1:len(secondParse[2])] + "_" + secondParse[3]
                
                #almostGeneName = tempParse[tempParse.find(".") + 1:len(tempParse)]

                # Write final header to file
                outputFile.write(geneName + "\n")

            else:

                # Write the sequence info underneath the file
                outputFile.write(line + "\n")
                
    
    # Close output file
    outputFile.close()

# Specify input directory path ############################################################## Change this when ready to do the whole dataset
filePath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\BlastProcessedResults\\"

# Get all files in the input directory
fileList = os.listdir(filePath)

# Goes one file above the input directory for creating an output directory
rootPath = filePath[0:filePath.rfind("\\")]

# Filters out any non fasta files
for f in fileList:
    if f.find(".fa") == -1:
        fileList.remove(f)

# If the output directory file is not already there, create one
if not os.path.exists(rootPath + "RenamedBlastFiles"):
    os.makedirs(rootPath + "RenamedBlastFiles")

# Creates the output directory path
outPath = rootPath + "RenamedBlastFiles\\"

# Loops through all files in the list and parses them by name
for f in fileList:
    blastRenamer(filePath + f)


