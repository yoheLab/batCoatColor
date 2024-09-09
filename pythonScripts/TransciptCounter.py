# This takes a FASTA query and uses the header to count the number of transcripts
def geneList(fileName):
    geneDict = {}
    
    # Open the file
    with open(fileName) as fileInput:
        
        # Break into rows
        for row in fileInput:
            
            # Uses the number of pipes to determine header, adjust as necessary
            if row.count("|") == 1:
                
                # This pulls the keys for the dictionary. Default is gene name but adjust as you'd like
                gene = ((str((row.rsplit("|"))[0])).strip("\n")).strip(">")
                
                # Adds gene name + transcript instance to dictionary
                if geneDict.get(gene) == None:
                    geneDict[gene] = 1
                    print (geneDict[gene])                
                else:
                    geneDict[gene] += 1
                    print (geneDict[gene])
    
    # Return the final dictionary
    return geneDict



# This function takes the dictionary created earlier and puts it into CSV format unordered.
def csvCreator(inputDict):
    tempString = ""
    
    # Accessing keys and building the first row of the table
    for key in inputDict:
        tempString += (key + ",")
    
    # Remove the comma at the end and create a new line
    tempString = tempString[:-1]
    tempString += "\n"
    
    # Accessing keys again to build the second line by referencing the dictionary
    for key in inputDict:
        tempString += (str(inputDict[key]) + ",")
    
    # Remove the last comma
    tempString = tempString[:-1]
    
    # Return the file data
    return tempString



# This function takes the dictionary created earlier and puts it into CSV format. It has the addition of providing the ability to input a file with the keys in the order you'd like them 
def csvOrderedCreator(inputDict, orderFile):
    tempStringUpper = ""
    tempStringLower = ""
    
    # Opens the file with the entry order
    with open(orderFile) as fileInput:
        
        # Breaks that file into rows
        for row in fileInput:
            
            # Break that row into individual values and put them in a list. Change the delimiter as necessary (usually \t or ,)
            brokenRow = (row.strip()).split("\t")
            
            # Goes through the entries specified in the order file and checks if they're present in the dictionary. Adds them to the output strings
            for value in brokenRow:
                if value in inputDict:
                    tempStringUpper += (str(value) + ",")
                    tempStringLower += (str(inputDict[value]) + ",")
                else: # For values in order file that aren't in the dictionary, default is 0
                    tempStringUpper += (str(value) + ",")
                    tempStringLower += "0,"
    
    # Remove commas on theend of strings
    tempStringUpper = tempStringUpper[:-1]
    tempStringLower = tempStringLower[:-1]
    
    # Build and return the final stirng data for the file
    finalString = (tempStringUpper + "\n" + tempStringLower)
    return finalString



# This function just writes to a file
def writeToFile(outputString, fileName):
    outputFile = open(fileName, "w")
    outputFile = outputFile.write(outputString)
    outputFile.close()



file = "wholeGene167.txt"
countedGenes = geneList(file)
#print("1. \n" + countedGenes)

# fileContent = csvCreator(countedGenes)
# print("2. \n" + fileContent)

correctFile = csvOrderedCreator(countedGenes, "excelOrder.txt")
print("3. \n" + correctFile)

writeToFile(correctFile, "167Genes.csv")