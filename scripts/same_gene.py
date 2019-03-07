import pandas as pd
import numpy as num
import os
from difflib import SequenceMatcher
import argparse




#Path1 = "/home/rhuang06/Documents/Annotation_pipeline/New/ORTH/"
#Path2 = "/home/rhuang06/Documents/Annotation_pipeline/"

# parsing the arguments and warning message
ap = argparse.ArgumentParser(description="Create log files for different gene names in each Orthologues file")
ap.add_argument("-path",required=True,
	help="Path of folder that containing all folders that have all Orthologues")
ap.add_argument("-outpath",required=True,
	help="Path of directory you want to put output files")

args = vars(ap.parse_args())
Path1=args["path"]
Path2=args["outpath"]

#make output dir
def makedir (path):
    if not os.path.exists(path + "Orthologues_with_different_name"): 
        os.mkdir(path + "Orthologues_with_different_name")


#strip "-" from lists
def comparable(l):
    for x in range(len(l)):
        l[x] = l[x].strip("-")
    return(l)

#caluate similarity of each name
def similar(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

#compare gene names in each gene            
def same_gene(path1,path2):
    folder = os.listdir(path1)
    for folder_name in folder:
        file = os.listdir(path1 + folder_name)
        for name in file:
            df = pd.read_csv(path1 + folder_name + "/" + name)
            gene_name = df["Gene name"]
            name_1 = name.strip(folder_name)
            name_2 = name_1.strip("_")
            name_3 = name_2.strip("csv")
            name_4 = name_3.strip(".")
            other_name = df[name_4 + " " + "gene name"]
            gene_name_new = gene_name.str.upper()
            comparable(gene_name_new)
            other_name_new = other_name.str.upper()
            comparable(other_name_new)
            #log = open(path2 + name.strip(".csv") + "_log.txt", "a+")
            sub_df = pd.DataFrame()
            if folder_name == "Human": #specific comparasion for human
                for term in range(len(gene_name_new)):
                    if gene_name_new[term] == "NONE":
                        pass 
                    elif other_name_new[term] == "NONE":
                        pass   
                    else: 
                        if other_name_new[term] not in gene_name_new[term]:
                            score = similar(other_name_new[term],gene_name_new[term]) # give score for string similarity
                            temp_df = pd.DataFrame(list(df.loc[[term]].values), list(df.columns.values)) #change column names of dataframe
                            sub_df = sub_df.append(temp_df, ignore_index=True) #output the different gene names in to csv files
                            continue
            if folder_name == "Mouse": #specific comparasion for mouse
                for term in range(len(gene_name_new)):
                    if gene_name_new[term] == "NONE":
                        pass 
                    elif other_name_new[term] == "NONE":
                        pass   
                    else: 
                        if other_name_new[term] not in gene_name_new[term]:
                            score = similar(other_name_new[term],gene_name_new[term])
                            temp_df = pd.DataFrame(list(df.loc[[term]].values), list(df.columns.values))
                            sub_df = sub_df.append(temp_df, ignore_index=True)
                            continue
            else:
                for term in range(len(gene_name_new)):
                    if gene_name_new[term] == "NONE":
                        pass 
                    elif other_name_new[term] == "NONE":
                        pass   
                    else: 
                        if other_name_new[term] not in gene_name_new[term]:
                            score = similar(other_name_new[term],gene_name_new[term])
                            temp_df = pd.DataFrame(list(df.loc[[term]].values))
                            sub_df = sub_df.append(temp_df)
                            continue
            #sub_df = pd.DataFrame(sub_df,columns=list(df.columns.values))
            sub_df = sub_df.rename(index=str, columns={0: df.columns.values[0], 1: df.columns.values[1], 2: df.columns.values[2], 3:df.columns.values[3]}) # rename columns 
            sub_df = sub_df.loc[:,~sub_df.columns.duplicated()]
            sub_df.to_csv(path2 + "Orthologues_with_different_name" + "/" + name, index = None, header=True)  #output as csv file
             
makedir(Path2)                    
same_gene(Path1,Path2)
            
        
        

                        

        
        