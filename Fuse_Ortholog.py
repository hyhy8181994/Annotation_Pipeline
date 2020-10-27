import pandas as pd
import numpy as num
import os
import difflib 
import argparse
import warnings

#Path = "/home/rhuang06/Documents/Annotation_pipeline/Proccessed_Data"
ap = argparse.ArgumentParser(description="Fuse Ensembl orthologues file with OMA orthologues file if there is extra information found in OMA files")

ap.add_argument("-path",required=False,
	help="Path of folder that containing all folders that have all Orthologues")
ap.add_argument("-outpath",required=False,
	help="Path of directory you want to put output files")

args = vars(ap.parse_args())
Path1=args["path"]
Path2=args["outpath"]


Path1 = "/home/rhuang06/Documents/Annotation_pipeline/Proccessed_Data"


#load oma files
def read_oma(omapath,folder,o_file):
    oo_file = o_file.split(".")
    animal_name = oo_file[0].split("_")
    if "Goat" in animal_name:
        oma_df = "None"
    else:
        oma_df = pd.read_csv(omapath + "/" + "OMA" + "/" + folder + "/" + oo_file[0] + ".txt")    
    return(oma_df)

#try to fuse OMA files to Ensembl files if there is extra information in oma files
def fuse(path):
    folders = ["ORTH","OMA"]
    for folder in folders:
        if folder == "ORTH":
            subfolders = os.listdir(path + "/" + folder)
            for subfolder in subfolders:
                files = os.listdir(path + "/" + folder + "/" + subfolder)
                for file in files:
                    df = pd.read_csv(path + "/" + folder + "/" + subfolder + "/" + file)                                      
                    df_oma = read_oma(path,subfolder,file)
                    df_sub = df.iloc[:,[0,2]]
                    if "frame" in str(type(df_oma)):
                        df_oma_sub = df_oma.iloc[:,[0,2]]
                        df_sub.append(df_oma_sub)
                    df_sub = df_sub.drop_duplicates()                                        
                    if df_sub.shape[0] == df.shape[0]:
                        print("\nNo extra ortholog found for " + file +"\n")
                        end = "end"                        
                    else:
                        df_sub = df_sub.sort_values(by = "Gene stable ID")                        
                        df.where((df["Gene stable ID"] == df_sub["Gene stable ID"]), other = num.nan) 
    if end == "end":
        print("\nNothing is produced\n")
                        
                    

warnings.simplefilter(action='ignore', category=FutureWarning)                   
                    

fuse(Path1)
            