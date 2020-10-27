import pandas as pd
import os
import warnings
import argparse
import pickle
import time

#Path1 = '/home/rhuang06/Documents/Annotation_pipeline/Proccessed_Data/ORTH'
#Path2 = "/home/rhuang06/Documents/Annotation_pipeline"
#ori_Path = Path2 + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Fuse_orth_file.csv"
#index_Path = Path2 + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Cliquer_index_file.csv"


# parsing the arguments and warning message
ap = argparse.ArgumentParser(description="Produce index file with all orthologue gene ID from orth files. \nRemove repeated orthologues and reduce file number")
ap.add_argument("-path",required=False,
	help="Path of folder that containing all folders that have all Orthologues")
ap.add_argument("-outpath",required=False,
	help="Path of directory you want to put output files")

args = vars(ap.parse_args())
Path1=args["path"]
Path2=args["outpath"]

Path1 = '/home/rhuang06/Documents/Annotation_pipeline/Proccessed_Data/ORTH'
Path2 = "/home/rhuang06/Documents/Annotation_pipeline"
Path3 = Path2 + "/Proccessed_Data/Fuse_Orth_file/one2one_orthologs"

#make directory
def make_dir(path):
    if not os.path.exists(path + "/" + "Proccessed_Data" + "/" + "Fuse_Orth_file"): 
        os.mkdir(path + "/" + "Proccessed_Data" + "/" + "Fuse_Orth_file")
    if not os.path.exists(path + "/" + "Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Reduced_orth"):
        os.mkdir(path + "/" + "Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Reduced_orth")
    if not os.path.exists(path + "/" + "Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Reduced_one2one_orth"):
        os.mkdir(path + "/" + "Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Reduced_one2one_orth")
    if not os.path.exists(path + "/" + "Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "one2one_orthologs"):
        os.mkdir(path + "/" + "Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "one2one_orthologs")


    

#Produce index file with all orthologous gene ID from orth files 
def fuse(path1,path2,mode):
    folder = os.listdir(path1)
    folder.sort()
    #final_df = pd.DataFrame()
    final_index_df = pd.DataFrame()
    #fuse_df_s = pd.DataFrame()
    print("Preparing ortholog index file\n")
    for folder_name in folder:
        file = os.listdir(path1 + "/" + folder_name)
        file.sort()
        #fuse_df_s = pd.DataFrame()
        fuse_df = pd.DataFrame()        
        for name in file:
            print("Processing {}\n".format(name))
            name1 = name.split(".")[0]
            name2 = name1.split("_")[1]
            name3 = name1.split("_")[0]
            df = pd.read_csv(path1 + "/" + folder_name + "/" + name)
            df1 = df[df[name2 + " gene stable ID"] != "None"]
            df1 = df1.rename(index=str, columns={(name2 + " gene stable ID"): "Orth ID", (name2 + " gene name"): "Orth gene name"})
            fuse_df = fuse_df.append(df1,ignore_index=True)
            fuse_df = fuse_df.drop_duplicates()
            fuse_df_1 = fuse_df[["Gene stable ID"]]
            final_index_df = final_index_df.append(fuse_df_1,ignore_index= True)            
        final_index_df = final_index_df.drop_duplicates()
    final_index_df["Number"] = list(range(1,final_index_df.shape[0]+1))
    final_index_df.to_csv(path2 + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Cliquer_index_" + mode + "_file.csv", index = None, header=True)
    

def one_2_one(path,outpath):
    folder = os.listdir(path)
    folder.sort()
    if not os.path.exists(outpath + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "one2one_orthologs"):
        os.mkdir(outpath + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "one2one_orthologs")    
    for folder_name in folder:
        if not os.path.exists(outpath + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "one2one_orthologs" + "/" + folder_name):
            os.mkdir(outpath + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "one2one_orthologs" + "/" + folder_name)
        file = os.listdir(path + "/" + folder_name)
        file.sort()
        for f in file:
            df = pd.read_csv(path + "/" + folder_name + "/" + f)
            name = f.split(".")[0]
            name1 = name.split("_")[0]
            name2 = name.split("_")[1]
            df1 = df[df[name2 + " homology type"] == "ortholog_one2one"]
            df1.to_csv(outpath + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "one2one_orthologs" + "/" + folder_name + "/" + f, index = None, header = True)




#Remove repeated orthologs and reduce file number
def remove(path1,path2,mode):
    folder = os.listdir(path1)
    folder.sort()
    looked_list = list()
    print("Removing repeated orthologs\n")
    for f in folder:
        files = os.listdir(path1 + "/" + f)
        files.sort()
        if len(looked_list) == 0:
            pass
        else:
            for item in looked_list:
                file_name = f + "_" + item + ".txt"
                files.remove(file_name)
        for file in files:
            print("Processing {} \n".format(file))
            name = file.split(".")[0]
            name1 = name.split("_")[0]
            name2 = name.split("_")[1]
            name1 = name.split("_")[0]
            name2 = name.split("_")[1]
            df1 = pd.read_csv(path1 + "/" + f + "/" + file)
            df2 = pd.read_csv(path1 + "/" + name2 + "/" + name2 + "_" + name1 + ".txt")         
            df1 = df1[df1[name2 + " gene stable ID"] != "None"]
            df2 = df2[df2[name1 + " gene stable ID"] != "None"]
            df1 = df1[["Gene stable ID",name2 + " gene stable ID"]]
            df2 = df2[["Gene stable ID",name1 + " gene stable ID"]]
            df1 = df1.rename(index = str, columns = {(name2 + " gene stable ID"):"Orth ID"})            
            df2 = df2.iloc[:,::-1]
            df2 = df2.rename(index = str, columns = {(name1 + " gene stable ID"):"Gene stable ID", "Gene stable ID":"Orth ID"})
            df1 = df1.append(df2)
            df1 = df1.drop_duplicates()
            if mode == "all":
                df1.to_csv(path2 + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Reduced_orth" + "/" + file, index = None, header=True)
            elif mode == "one":
                df1.to_csv(path2 + "/" + "Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Reduced_one2one_orth" + "/" + file, index = None, header=True)
        looked_list.append(f)
        

#Prepare GO term library for gene annontation
def load():
    print("Preparing GO term library")
    GO_files = os.listdir(Path2 + "/Proccessed_Data/GOD/")
    fuse_df = pd.DataFrame()
    for GO_file in GO_files:
        df = pd.read_csv(Path2 + "/Proccessed_Data/GOD/" + GO_file)
        df = df.loc[:,["Gene stable ID","GO term accession"]]
        fuse_df = fuse_df.append(df)
    fuse_df.to_csv(Path2 + "/Proccessed_Data/Fuse_Orth_file/GO_fuse_file.csv", index= None, header= True)
    print("GO term library preparation finished\n")

    print("Save GO fuse file to dictionary")
    fuse_id = list(fuse_df["Gene stable ID"].drop_duplicates())
    fuse_dict = dict()
    fuse_du_go = fuse_df[fuse_df["Gene stable ID"].duplicated(keep=False)]
    fuse_un_go = fuse_df[fuse_df["Gene stable ID"].duplicated(keep=False) == False]
    fuse_un_go_term = list(fuse_un_go["GO term accession"])
    fuse_un_go_term = [[i] for i in fuse_un_go_term]
    fuse_un_dict = dict(zip(list(fuse_un_go["Gene stable ID"]),fuse_un_go_term))
    index_list = range(fuse_du_go.shape[0])
    fuse_du_list = list()
    fuse_du_dict = dict()
    for d in index_list:
        current = fuse_du_go.iloc[d,:]
        try:
            next_term = fuse_du_go.iloc[d + 1,:]
        except:
            fuse_du_list.append(current["GO term accession"])
            fuse_temp_dict = {current["Gene stable ID"]:fuse_du_list}
            fuse_du_dict.update(fuse_temp_dict)
            break 
        if current["Gene stable ID"] == next_term["Gene stable ID"]:
            fuse_du_list.append(current["GO term accession"])          
        else:
            fuse_du_list.append(current["GO term accession"])
            fuse_temp_dict = {current["Gene stable ID"]:fuse_du_list}
            fuse_du_list = list()
            fuse_du_dict.update(fuse_temp_dict)
            continue
    fuse_un_dict.update(fuse_du_dict)

    with open(Path2 + '/Proccessed_Data/Fuse_Orth_file/temp_GO_fuse.dat',"wb") as handle:
        pickle.dump(fuse_un_dict,handle,protocol=pickle.HIGHEST_PROTOCOL)

start = time.time()
warnings.simplefilter(action='ignore', category=FutureWarning)                   

make_dir(Path2)
#load()
one_2_one(Path1,Path2)
#fuse(Path1,Path2,"all")
fuse(Path3,Path2,"one")
remove(Path3,Path2,"one")
#remove(Path1,Path2,"all")
end = time.time()-start
print("Process finished cost {} min".format(end/60))