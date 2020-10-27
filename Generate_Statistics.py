import pandas as pd
import numpy as np
import os
import sys
import argparse
import csv



# parsing the arguments
ap = argparse.ArgumentParser(description="Create log files for different gene names in each Orthologues file")
ap.add_argument("-path",required=False,
	help="Path of folder that containing all folders that have all data")
ap.add_argument("-outpath",required=False,
	help="Path of directory you want to put output file")

args = vars(ap.parse_args())
Path=args["path"]
out=args["outpath"]

Path = "/home/rhuang06/Documents/Annotation_pipeline/Proccessed_Data"
out = "/home/rhuang06/Documents/Annotation_pipeline"
#sys.stdout = open(out + "/" + "stats.txt", "w")

Path_1 = Path + "/Fuse_Orth_file/one2one_orthologs/"
def stats (path):
    folder_list = os.listdir(path)
    same_name_list = []    
    same_count = []
    orth_dict = dict()
    same_dict = dict()
    oma_dict = dict()
    GO_list = list()
    one2one_orth = dict()
    for folder in folder_list:
        files = os.listdir(path + "/" + folder)
        if folder == "OMA":
            print("##############number of orthologues###############")
            print("######" + folder + "######")
            OMA_folder = os.listdir(path + "/" + folder)
            OMA_folder.sort()
            for OMA_subfolder in OMA_folder:
                OMA_files = os.listdir(path + "/" + folder + "/" + OMA_subfolder)           
                OMA_files.sort()
                temp_dict = dict()
                for OMA_file in OMA_files:
                    table = pd.read_csv(path + "/" + folder + "/" + OMA_subfolder + "/" + OMA_file, engine='python')
                    table_sub = table.iloc[:,0:1].drop_duplicates()
                    total_rows = table_sub.count
                    total_rows = table_sub.shape[0]
                    root = OMA_file.split(".")[0]
                    print(root)
                    print(total_rows)
                    temp_dict = {root : total_rows}
                    oma_dict.update(temp_dict)                 
        if folder == "ORTH":
            print("################number of orthologues#############")
            print("########" + folder + "#########")
            ORTH_folder = os.listdir(path + "/" + folder)
            ORTH_folder.sort()
            for ORTH_subfolder in ORTH_folder:
                orth_temp_dict = dict()
                ORTH_files = os.listdir(path + "/" + folder + "/" + ORTH_subfolder)
                ORTH_files.sort()
                for ORTH_file in ORTH_files:
                    table = pd.read_csv(path + "/" + folder + "/" + ORTH_subfolder + "/" + ORTH_file)
                    table_sub = table.iloc[:,[0,2]]
                    table_drop = table_sub[table_sub.iloc[:,1] != "None"]
                    root = ORTH_file.split(".")[0]
                    temp_dict = {root:table_drop.shape[0]}
                    orth_temp_dict.update(temp_dict)
                    print(root)
                    print(table_drop.shape[0])
                orth_dict.update(orth_temp_dict)
        if (folder == "GOD") or (folder == "PC"):
            print("###############GO term count#############")
            if folder == "PC":
                print("#########protein coing gene#######")
            files = os.listdir(path + "/" + folder)
            files.sort()
            for GOD_files in files:          
                table = pd.read_csv(path + "/" + folder + "/" + GOD_files)                                                                 
                root = GOD_files.split("_")[0]
                go = table[table["GO term accession"] != "None"]
                n_gene_GO = go['Gene stable ID'].drop_duplicates()
                un_ID = table['Gene stable ID'].drop_duplicates()
                per = ((n_gene_GO.shape[0])/un_ID.shape[0])*100
                print(root)
                print("number of gene " + str(un_ID.shape[0]))
                print("number of GO terms " + str(go.shape[0]))
                print("number of gene with GO " + str(n_gene_GO.shape[0]))
                print("percent of gene GO " + str(per) + "%")
                temp_list = [str(un_ID.shape[0]),str(go.shape[0]),str(n_gene_GO.shape[0]),str(per) + "%"]
                GO_list.append(temp_list)                
        if folder == "GO":
            print("################Gene count##############")
            files = os.listdir(path + "/" + folder)
            files.sort()
            for GO_files in files:          
                table = pd.read_csv(path + "/" + folder + "/" + GO_files)                                                 
                root = GO_files.split("_")[0]
                table = table.iloc[:,[0,1]]
                un_ID = table['Gene stable ID'].drop_duplicates()
                print(root)
                print("number of gene " + str(un_ID.shape[0]))
        if folder == "Orthologues_with_same_name":
            print("###############same_gene_name###############")
            same_files = os.listdir(path + "/" + folder) 
            same_files.sort()
            print(same_files)
            for same_file in same_files:
                temp_dict = dict()
                table = pd.read_csv(path + "/" + folder + "/" + same_file)
                total_rows = table.count
                total_rows = table.shape[0]
                root = same_file.split(".")[0]
                print(root)
                print(total_rows)
                temp_dict = {root : total_rows}
                same_dict.update(temp_dict)
                same_name_list.append(root)
                same_count.append(total_rows)
        if folder == "Orthologues_with_different_name":
            print("###############different_gene_name###############")
            different_files = os.listdir(path + "/" + folder)           
            different_files.sort()
            for different_file in different_files:
                table = pd.read_csv(path + "/" + folder + "/" + different_file)
                total_rows = table.count
                total_rows = table.shape[0]
                root = different_file.split(".")[0]
                print(root)
                print(total_rows)
                #diff_name_list.append(root)
                #diff_count.append(total_rows)
    

    def make_df(o_dict,n,name,out_path):
        o_list = list(o_dict.values())
        o_list = [o_list[i:i + n] for i in range(0, len(o_list), n)]
        counter = 0
        for sub in o_list:
            sub.insert(counter,"-")
            counter += 1        
        df = pd.DataFrame(o_list)
        number_list = list(range(n+1))        
        sci_name = ['Gallus gallus','Bos taurus','Capra hircus','Equus caballus','Homo sapiens','Mus musculus','Sus scrofa','Ovis aries']
        if name == "OMA":
            sci_name = ['Gallus gallus','Bos taurus','Equus caballus','Homo sapiens','Mus musculus','Sus scrofa','Ovis aries']
        name_for_df = dict(zip(number_list,sci_name))
        df.rename(columns = name_for_df, index = name_for_df, inplace = True)
        df.to_csv(out_path + "/" + name + "_table.csv")
    one_folder = os.listdir(Path_1)
    print("###########one to one orthologs###########")
    one_folder.sort()
    for one_f in one_folder:
        print(one_f)
        one_files = os.listdir(Path_1 + one_f)
        one_files.sort()
        one_orth_temp_dict = dict()
        for one_file in one_files:        
            table = pd.read_csv(Path_1 + one_f + "/" + one_file)
            table_sub = table.iloc[:,[0,2]]
            table_drop = table_sub[table_sub.iloc[:,1] != "None"]
            root = one_file.split(".")[0]
            temp_dict = {root:table_drop.shape[0]}
            one_orth_temp_dict.update(temp_dict)
            print(root)
            print(table_drop.shape[0])
        one2one_orth.update(one_orth_temp_dict)
            



        
    make_df(orth_dict,7,"Ortholog",out)
    make_df(same_dict,7,"Same name",out)
    make_df(oma_dict,6,"OMA",out)
    make_df(one2one_orth,7,"One2one",out)
    GO_df = pd.DataFrame(GO_list)
    GO_column = dict(zip(list(range(4)),["Gene Count",'GO Count','Gene with GO count','Percentage of gene with GO']))
    GO_row = dict(zip(list(range(16)),['Gallus gallus','Bos taurus','Capra hircus','Equus caballus','Homo sapiens','Mus musculus','Sus scrofa','Ovis aries','Gallus gallus','Bos taurus','Capra hircus','Equus caballus','Homo sapiens','Mus musculus','Sus scrofa','Ovis aries']))
    GO_df.rename(columns = GO_column,index = GO_row, inplace = True)
    GO_df.to_csv(out + "/" + "GO_table.csv") 
    print("Totall number of same gene name found")
    print(sum(same_count))    


            

                

            
stats(Path)
       
