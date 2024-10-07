import os
import matplotlib.pyplot as plt
import pandas

def matchPartCount(files):
    count = 1

    # Isolates part## where # is a number from a gene name file
    
    if len(files) == 1:
        return count
    
    else:
        firstPart = files[0][(files[0].find("part")):files[0].find("ENSG") - 1]
        
        print(files)

        for f in files[1:]:
            newPart = f[(f.find("part")):f.find("ENSG") - 1]
            if newPart == firstPart:
                return count
            else:
                count += 1
    
    # For situations where there is only one species but multiple match parts
    return count



def countGenes(folders):
    tempDict = {}
    for folder in folders:

        files = os.listdir(baseFolderPath + "\\" + folder)
        #matchPartNumber = matchPartCount(files)
        
        if folder.split("_")[0] == "RAB7A":
            print(folder.split("_")[0])
        
        tempDict.update({folder.split("_")[0]: len(files)})

    return tempDict


#no filter
#baseFolderPath = "G:\\Other computers\\DeepThought\\Wormhole\\Yohe_Lab\\BlastE0\\LongestDedupeIsolatedGenes"
#baseFolderPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\BlastE0\\LongestDedupeIsolatedGenes"

# 1e-15
#baseFolderPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\BlastE15\\LongestDedupeIsolatedE15Genes"

# 1e-30
baseFolderPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\BlastE30\\LongestDedupeIsolatedE30Genes"


# 1e-50
#baseFolderPath = "G:\\Other computers\\DeepThought\\Wormhole\\Yohe_Lab\\BlastE50\\LongestDedupeIsolatedE50Genes"
#baseFolderPath = "C:\\Users\\Jacob\\Desktop\\Wormhole\\Yohe_Lab\\BlastE50\\LongestDedupeIsolatedE50Genes"




folders = os.listdir(baseFolderPath)

geneCountDict = countGenes(folders)

df = pandas.DataFrame.from_dict(geneCountDict, orient="index")

#df.sort_values(by="0", ascending=False)

df1 = df.rename(columns={df.columns[0] : 'numberOfGenes'})

print(df1)

df2 = df1.sort_values(by="numberOfGenes", ascending=False)

#print(df[0])
"""
plt.bar(df2.index.values, df2["numberOfGenes"], width=0.5, color="purple")
plt.title("Hits Per Gene Blast 1e-50 Filter")

"""
#plt.bar(range(len(geneCountDict)), list(geneCountDict.values()), tick_label=list(geneCountDict.keys()), y=0)
#plt.xticks(rotation="vertical")

fig, ax = plt.subplots()

ax.barh(df2.index.values, df2["numberOfGenes"], align="center", color="purple", height=0.8,)

#for s in ['top', 'right']:
#    ax.spines[s].set_visible(False)

ax.yaxis.set_ticks_position('none')

#ax.xaxis.set_tick_params(pad = 5)
#ax.yaxis.set_tick_params(pad = 10)


ax.invert_yaxis()

ax.set_ymargin(0.0000001)

ax.set_title("Hits Per Gene Blast 1e-30 (" + str(len(df2["numberOfGenes"])) + " Genes Total)", loc ='Center', fontsize=24)

plt.yticks(fontsize=6)

plt.ylabel("Gene Name", fontsize=24)
plt.xlabel("Hits/Species Found Per Gene", fontsize=24)

plt.show()
