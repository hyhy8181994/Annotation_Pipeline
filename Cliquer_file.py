import pandas as pd
import numpy as np
import multiprocessing
import time 
import os
import argparse



#Path1 = '/home/rhuang06/Documents/Annotation_pipeline/Proccessed_Data/ORTH'
#Path2 = "/home/rhuang06/Documents/Annotation_pipeline"
#ori_Path = Path2 + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Fuse_orth_file.csv"
#index_Path = Path2 + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file" + "/" + "Cliquer_index_file.csv"
#Path3 = Path2 + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file"

# parsing the arguments and warning message
ap = argparse.ArgumentParser(description="Translate Ortholog gene ID to number index based on index file with multipleprocessing")
ap.add_argument("-path",required=False,
	help="Path of folder that containing all folders that have all Orthologues")
ap.add_argument("-outpath",required=False,
	help="Path of directory you want to put output files")
ap.add_argument("-n", required = False, help = "Number of processes for multiple processing")

args = vars(ap.parse_args())
Path1 = args["path"]
Path2 = args["outpath"]

Path1 = '/home/rhuang06/Documents/Annotation_pipeline/Proccessed_Data/ORTH'
Path2 = "/home/rhuang06/Documents/Annotation_pipeline"

Path3 = Path2 + "/" +"Proccessed_Data" + "/" + "Fuse_Orth_file"




#Transfer ortholog ID to number index based on index file
def transfer(item):    
    Path = Path3
    index_df = pd.read_csv(Path + "/Cliquer_index_file.csv", engine= "python")
    index_dict = dict(zip(index_df["Gene stable ID"],index_df["Number"]))
    file_list = os.listdir(Path + "/Reduced_orth")
    file_abspath_list = list()
    for f in file_list:
        f_absname = Path + "/Reduced_orth/" + f
        file_abspath_list.append(f_absname)    
    print("Processing " + "file " + os.path.basename(file_abspath_list[item]))
    with open(file_abspath_list[item],"r") as h:
        ori_file = h.readlines()
    #ori_df = pd.read_csv(file_abspath_list[item], engine= "python")
    name = os.path.basename(file_abspath_list[item])
    #number_list = []
    '''for id in range(ori_df.shape[0]):
        orth = list(ori_df.iloc[id,:])
        index1 = index_df.loc[index_df["Gene stable ID"] == orth[0]]
        index2 = index_df.loc[index_df["Gene stable ID"] == orth[1]]
        index1 = index1.values
        index1 = index1.tolist()
        index2 = index2.values
        index2 = index2.tolist()
        number = ["e",index1[0][1],index2[0][1]] #1:gene id 2:orth gene id  
        number_list.append(number)'''          
    cliq_file = open(Path + "/" + "file" + "/Cliquer_temp_" + name, "w+")
    for num,id in enumerate(ori_file):
        id_line = id.split(",")
        id_line = [id_line[0],id_line[1].strip("\n")]
        #print(id_line)
        if num != 0:
            cliq_line = "e,{},{}\n".format(index_dict[id_line[0]],index_dict[id_line[1]])
        else:
            cliq_line = ""
        cliq_file.write(cliq_line)
    cliq_file.close()
    
    #number_df = pd.DataFrame(number_list)
    #number_df.to_csv(Path + "/" + "file" + "/Cliquer_temp_" + name,index = None, header= False)
    print("file" + os.path.basename(file_abspath_list[item]) +" finished")

#Transfer ortholog ID to number index based on index file
def transfer_one(item):    
    Path = Path3
    index_df = pd.read_csv(Path + "/Cliquer_index_one_file.csv", engine= "python")
    index_dict = dict(zip(index_df["Gene stable ID"],index_df["Number"]))
    file_list = os.listdir(Path + "/Reduced_one2one_orth")
    file_abspath_list = list()
    for f in file_list:
        f_absname = Path + "/Reduced_one2one_orth/" + f
        file_abspath_list.append(f_absname)
    print("Processing " + "file " + os.path.basename(file_abspath_list[item]))
    with open(file_abspath_list[item],"r") as h:
        ori_file = h.readlines()
    name = os.path.basename(file_abspath_list[item])
    cliq_file = open(Path + "/" + "one_file" + "/Cliquer_one_temp_" + name, "w+")
    for num,id in enumerate(ori_file):
        id_line = id.split(",")
        id_line = [id_line[0],id_line[1].strip("\n")]
        #print(id_line)
        if num != 0:
            cliq_line = "e,{},{}\n".format(index_dict[id_line[0]],index_dict[id_line[1]])
        else:
            cliq_line = ""
        cliq_file.write(cliq_line)
    cliq_file.close()        
    #number_df = pd.DataFrame(number_list)
    #number_df.to_csv(Path + "/" + "one_file" + "/Cliquer_one_temp_" + name,index = None, header= False)
    print("file " + os.path.basename(file_abspath_list[item]) +" finished")

def fuse_file(path,mode):
    if mode == "all":
        files = os.listdir(path + "/" + "file")
        files.sort()
        fuse = pd.DataFrame()
        print("\nFuse files")
        for file in files:
            df = pd.read_csv(path + "/" + "file" + "/" + file, header= None)
            fuse = fuse.append(df)
        fuse.to_csv(path + "/" + "Cliquer_temp_file.csv", index = False, header = False)
    elif mode == "one":
        files = os.listdir(path + "/" + "one_file")
        files.sort()
        fuse = pd.DataFrame()
        print("\nFuse files")
        for file in files:
            df = pd.read_csv(path + "/" + "one_file" + "/" + file, header= None)
            fuse = fuse.append(df)
        fuse.to_csv(path + "/" + "Cliquer_temp_one_file.csv", index = False, header = False)

def top_line(path,out,mode):
    if mode == "all":
        df = pd.read_csv(path, header = None)
        column1 = df.iloc[:,1]
        column2 = df.iloc[:,2]
        column = column1.append(column2)
        column = column.drop_duplicates()
        number_node = column.shape[0]
        number_edge = df.shape[0]
        df2 = pd.DataFrame([["p",number_node,number_edge]])
        df2 = df2.append(df)
        df2.to_csv(out + "/" + "Final_Cliquer_file.csv", index = None, header =False)
    elif mode == "one":
        df = pd.read_csv(path, header = None)
        column1 = df.iloc[:,1]
        column2 = df.iloc[:,2]
        column = column1.append(column2)
        column = column.drop_duplicates()
        number_node = column.shape[0]
        number_edge = df.shape[0]
        df2 = pd.DataFrame([["p",number_node,number_edge]])
        df2 = df2.append(df)
        df2.to_csv(out + "/" + "Final_Cliquer_one_file.csv", index = None, header =False)

    
def final_process(path,mode):
    if mode == "all":
        file = open(path + "/" + "Final_Cliquer_file.csv", "r")
        data = file.read()
        data = data.replace(","," ")
        with open(path + "/" + "Final_Cliquer_file.csv", "w+") as f:
            f.write(data)
        os.rename(path + "/" + "Final_Cliquer_file.csv", path + "/" + "Final_Cliquer_file.txt")
    elif mode == "one":
        file = open(path + "/" + "Final_Cliquer_one_file.csv", "r")
        data = file.read()
        data = data.replace(","," ")
        with open(path + "/" + "Final_Cliquer_one_file.csv", "w+") as f:
            f.write(data)
        os.rename(path + "/" + "Final_Cliquer_one_file.csv", path + "/" + "Final_Cliquer_one_file.txt")

def add_name(path,mode):
    if mode == "all":
        file = open(path + "/" + "Final_Cliquer_file.txt", "r")
        data = file.readline()
        data = data.split(" ")
        data.insert(1,"animal")
        data[0] = data[0] + " "
        data[1] = data[1] + " "
        data[2] = data[2] + " "
        data = "".join(data)
        oline = file.readlines()
        oline.insert(0,data)
        file = open(path + "/" + "Final_Cliquer_file.txt", "w")
        file.writelines(oline)
        file.close()
    elif mode == "one":
        file = open(path + "/" + "Final_Cliquer_one_file.txt", "r")
        data = file.readline()
        data = data.split(" ")
        data.insert(1,"animal")
        data[0] = data[0] + " "
        data[1] = data[1] + " "
        data[2] = data[2] + " "
        data = "".join(data)
        oline = file.readlines()
        oline.insert(0,data)
        file = open(path + "/" + "Final_Cliquer_one_file.txt", "w")
        file.writelines(oline)
        file.close()

#code for all orthologs
'''if __name__ == '__main__':
    start_time = time.time()
    length = os.listdir(Path3 + "/Reduced_orth")
    if not os.path.exists(Path3 + "/" + "file"):
        os.mkdir(Path3 + "/" + "file")
    pool = multiprocessing.Pool(processes=8)    
    pool.map(transfer,range(len(length)))
    pool.close()
    fuse_file(Path3,"all")
    top_line(Path3 + "/" + "Cliquer_temp_file.csv", Path3,"all")
    final_process(Path3,"all")
    add_name(Path3,"all")
    end_time = time.time() - start_time
    print("In total cost " + str((end_time/60)) + " mins")'''

#code for one to one orthologs
if __name__ == '__main__':
    start_time = time.time()
    length = os.listdir(Path3 + "/Reduced_one2one_orth")
    if not os.path.exists(Path3 + "/" + "one_file"):
        os.mkdir(Path3 + "/" + "one_file")
    pool = multiprocessing.Pool(processes=7)    
    pool.map(transfer_one,range(len(length)))
    pool.close()
    fuse_file(Path3,"one")
    top_line(Path3 + "/" + "Cliquer_temp_one_file.csv", Path3, "one")
    final_process(Path3,"one")
    add_name(Path3,"one")
    if os.path.exists(Path3 + "/" + "Cliquer_temp_one_file.csv") is True:
        os.remove(Path3 + "/" + "Cliquer_temp_one_file.csv")
    if os.path.exists(Path3 + "/" + "Cliquer_temp_file.csv") is True:
        os.remove(Path3 + "/" + "Cliquer_temp_file.csv")
    end_time = time.time() - start_time
    print("In total cost " + str((end_time/60)) + " mins")

