import os

# This method will replace a gene name from a file name with the gene name from it's parent folder
# Specifically, it replaces whatever is in between the first "." and "ENSG" of a file name
def fixName(folders):
    for folder in folders:
        geneName = folder[0:folder.find("_")]
        files = os.listdir(baseFolder + "\\" + folder)
        for file in files:
            
            os.rename(baseFolder + "\\" + folder + "\\" + file, baseFolder + "\\" + folder + "\\" + file[0:file.find(".") + 1] + geneName + file[file.find("ENSG") - 1:])

baseFolder = "G:\\Other computers\\DeepThought\\Wormhole\\Yohe_Lab\\BlastE50\\LongestDedupeIsolatedE50Genes"
folders = os.listdir(baseFolder)
fixName(folders)