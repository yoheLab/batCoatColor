import os
import matplotlib.pyplot as plt
import pandas

# This method loops through a list of folders and counts the number of files in each, returning a dictionary with the counts
def countGenes(folders):
    tempDict = {}
    for folder in folders:
        files = os.listdir(baseFolderPath + "\\" + folder)
        tempDict.update({folder.split("_")[0]: len(files)})

    return tempDict

# Method creates a horizontal bar plot representing the number of files present for a given gene
def makePlot(geneCounts, title):
    df = pandas.DataFrame.from_dict(geneCounts, orient="index")
    df = df.rename(columns={df.columns[0] : 'numberOfGenes'})
    df = df.sort_values(by="numberOfGenes", ascending=False)

    fig, ax = plt.subplots()

    ax.barh(df.index.values, df["numberOfGenes"], align="center", color="purple", height=0.8,)
    ax.yaxis.set_ticks_position('none')
    ax.invert_yaxis()
    ax.set_ymargin(0.0000001)
    ax.set_title(title + " (" + str(len(df["numberOfGenes"])) + " Genes Total)", loc ='Center', fontsize=24)

    plt.yticks(fontsize=6)
    plt.ylabel("Gene Name", fontsize=24)
    plt.xlabel("Hits/Species Found Per Gene", fontsize=24)

    plt.show()


# Main

# Folder paths
#no filter
#baseFolderPath = "G:\\Other computers\\DeepThought\\Wormhole\\Yohe_Lab\\BlastE0\\LongestDedupeIsolatedGenes"
#baseFolderPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\BlastE0\\"

# 1e-15
#baseFolderPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\BlastE15\\LongestDedupeIsolatedE15Genes"

# 1e-30
baseFolderPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\BlastE30\\LongestDedupeIsolatedE30Genes"

# 1e-50
#baseFolderPath = "G:\\Other computers\\DeepThought\\Wormhole\\Yohe_Lab\\BlastE50\\LongestDedupeIsolatedE50Genes"
#baseFolderPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\BlastE50\\LongestDedupeIsolatedE50Genes"

folders = os.listdir(baseFolderPath)
geneCountDict = countGenes(folders)
graphTitle = "Hits Per Gene Blast 1e-30"

makePlot(geneCountDict, graphTitle)