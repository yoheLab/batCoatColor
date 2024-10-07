import os

def fixName(folders):
    for folder in folders:
        geneName = folder[0:folder.find("_")]
        files = os.listdir(baseFolder + "\\" + folder)
        for file in files:
            
            #print(baseFolder + "\\" + folder + "\\" + file[0:file.find(".") + 1] + geneName + file[file.find("ENSG") - 1:])

            os.rename(baseFolder + "\\" + folder + "\\" + file, baseFolder + "\\" + folder + "\\" + file[0:file.find(".") + 1] + geneName + file[file.find("ENSG") - 1:])

baseFolder = "G:\\Other computers\\DeepThought\\Wormhole\\Yohe_Lab\\BlastE50\\LongestDedupeIsolatedE50Genes"
folders = os.listdir(baseFolder)
fixName(folders)