import pandas as pd
import argparse
import os
import numpy


# parsing the arguments and warning message
ap = argparse.ArgumentParser(description="Make obsoleted GO term table and remove obsoleted items in GO file")
ap.add_argument("-obo",required=False,
	help="Path of ontology file eg. go_basic.obo")
ap.add_argument("-path",required=False,
	help="Path of folder that containing all folders that have all Orthologues, GO datas")
ap.add_argument("-outpath",required=False,
	help="Path of directory you want to put output file")

args = vars(ap.parse_args())

file=args["obo"]
Path1=args["path"]
out_path=args["outpath"]

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

#Make new folders for output files
#path1 = path of originial files; path2 = path of directory for new folder
def make_dir(path1,path2):
    Folder =  ["GOD","GO","OMA","ORTH","PC"]    
    New_folder = "Proccessed_Data"
    if not os.path.exists(path2 + "/" + New_folder):
        os.mkdir(path2 + "/" + New_folder)
    for i in Folder:
        if not os.path.exists(path2 + "/" + New_folder + "/" + i):
            os.mkdir(path2 + "/" + New_folder + "/" + i)
        if i == "ORTH":
            file = os.listdir(path1 + "/" + i)
            for animal in file:
                if not os.path.exists(path2 + "/" + New_folder + "/" + i + "/" + animal):
                    os.mkdir(path2 + "/" + New_folder + "/" + i + "/" + animal)
        if i == "OMA":
            file1 = os.listdir(path1 + "/" + i)
            for animalx in file1:
                if not os.path.exists(path2 + "/" + New_folder + "/" + i + "/" + animalx):
                    os.mkdir(path2 + "/" + New_folder + "/" + i + "/" + animalx)
        
        
            

#Replace the empty well in data to None
# path = "path of directory with original files"
def get_none(path,out):
    file = os.listdir(path)
    print("\nReplacing empty data to None\n")
    for i in file:
        if i == "ORTH":
            files1 = os.listdir(path + "/" + i)
            for name in files1:
                files2 = os.listdir(path + "/" + i + "/" + name)
                for name1 in files2:
                    df = pd.read_csv(path + "/" + i + "/" + name + "/" + name1)          
                    df1 = df.where((pd.notnull(df)),"None")
                    df1.to_csv(out + "/" + "Proccessed_Data" + "/" + i + "/" + name + "/" + name1, index = None, header=True)
        elif i == "OMA":
            files1 = os.listdir(path + "/" + i)
            for name in files1:
                files2 = os.listdir(path + "/" + i + "/" + name)
                for name1 in files2:
                    name1_split = name1.split(".")
                    raw_name1 = name1_split[0].split("_")
                    oma_back = raw_name1[1]
                    oma_name = oma_back + " gene stable ID" 
                    df = pd.read_table(path + "/" + i + "/" + name + "/" + name1)          
                    df1 = df.where((pd.notnull(df)),"None")
                    df1.columns = ["Gene stable ID",oma_name, "Type", "OMA name"]                   
                    df1.to_csv(out + "/" + "Proccessed_Data" + "/" + i + "/" + name + "/" + name1, index = None, header=True)
        elif i == "GO":        
            files1 = os.listdir(path + "/" + i)
            for name in files1:
                df = pd.read_csv(path + "/" + i + "/" + name)         
                df1 = df.where((pd.notnull(df)),"None")
                df1.to_csv(out + "/" + "Proccessed_Data" + "/" + i + "/" + name, index = None, header=True)
        elif i == "GOD":        
            files1 = os.listdir(path + "/" + i)
            for name in files1:
                df = pd.read_table(path + "/" + i + "/" + name)          
                #skip the None value
                df1 = df.where((pd.notnull(df)),"None")
                df1.to_csv(out + "/" + "Proccessed_Data" + "/" + i + "/" + name, index = None, header=True)
        elif i == "PC":        
            files1 = os.listdir(path + "/" + i)
            for name in files1:
                df = pd.read_csv(path + "/" + i + "/" + name)         
                df1 = df.where((pd.notnull(df)),"None")
                df1.to_csv(out + "/" + "Proccessed_Data" + "/" + i + "/" + name, index = None, header=True)

#get_none("/home/rhuang06/Documents/Annotation_pipeline/Data","/home/rhuang06/Documents/Annotation_pipeline")

Path1 = "/home/rhuang06/Documents/Annotation_pipeline/Data"
file = "/home/rhuang06/Documents/Annotation_pipeline/go-basic.obo"
out_path = "/home/rhuang06/Documents/Annotation_pipeline"


#create a csv file of obsolete GO ID and replacement ID from GO_basic.obo
def obsolete_table (file_path,outfile_path):
    id_GO = []
    id_ob = []
    table = dict()
    n = 0  #counter one for making GO id
    n1 = 0 # counter two for making obsoleted GO term id
    print("\nPerparing obsolete GO term ID table\n")
    with open(file_path, "r") as f:
        for line in f:
            if "id: GO:" in line:
                id = line
                if "alt_id" in id:
                    id = " "
                else:
                    id1 = id.strip("id:")
                    id2 = id1.strip("\n")
                    id3 = id2.strip(" ")
                    id_GO.insert(n, id3)
                    n += 1 # counter 1
            if "is_obsolete: true" in line:
                id4 = id_GO[n - 1] #get n from last step
                id_ob.insert(n1, id4) #counter 2
                n1 += 1
                replace = []
                n2 = 0 #set up counter 3 for constructing list of replace GO term for obsoleted GO term
                for x in range(6):
                    next_line = next(f)
                    if "consider:" in next_line:
                        replace.insert(n2, next_line)
                        n2 += 1
                        n3 = 0 # set up counter 4 for reconstructing replacement GO id after cleaning
                        replace_re = []
                        for i in replace:
                            a = i.strip("\n")
                            b = a.strip("consider: ")
                            replace_re.insert(n3, b)
                            n3 += 1
                        #for i in replace_re:
                        t1 = {id4: replace_re}
                        table.update(t1)
                    else:
                        if n2 == 0:
                            no = "None"
                            t2 = {id4: no}
                            table.update(t2)   
    df = pd.DataFrame(list(table.items()), columns=["Obsolete GO term", "Replace GO term"])
    df.to_csv(outfile_path + "/" + "ob_table.csv",index = None, header=True)
    return(table)

#replace the obsoleted GO id in every orthologue 
def remove_ob(p1,p2,f,input_dict):
    file = os.listdir(p2 + "/" + "Proccessed_Data" + "/" + f + "/")
    #OB_table = pd.read_csv(p2 + "/" + "ob_table.csv")
    OB_table = input_dict
    ob_id = list(OB_table.keys())
    found_ob_id = []
    counter_one = 0
    for name in file:
        df1 = pd.read_csv(p2 + "/" + "Proccessed_Data" + "/" + f + "/" + name)
        na = str(name)
        access_name = df1["GO term accession"]
        print("Accessing" + " " + na)
        list_acc = list(access_name)
        for acc_id in list_acc:
            for id in ob_id:            
                if acc_id == id:
                    found_ob_id.insert(counter_one,acc_id)
                    counter_one += 1
        found_ob_id = list(dict.fromkeys(found_ob_id))
        if len(found_ob_id) != 0:
            print("Found obsolete GO term ID")
            print(found_ob_id)
            for found_id in found_ob_id:
                row_id = list(df1.loc[df1['GO term accession'] == found_id].index.values)
                #replace_id = OB_table[OB_table["Obsolete GO term"] == found_id].iloc[0]["Replace GO term"]
                replace_id = OB_table[found_id]
                for i in row_id:
                    df1.loc[i,'GO term accession']=replace_id
                    if replace_id == "None":
                        df1.loc[i,'GO term name']="None"
                        df1.loc[i,'GO term definition']="None"
        else:
            print("No obsolete GO term found")
        df1.to_csv(p2 + "/" + "Proccessed_Data" + "/" + f + "/" + name, index = None, header=True)



make_dir(Path1,out_path)

get_none(Path1,out_path)

ob_dict = obsolete_table(file,out_path)
obsolete_table(file,out_path)

remove_ob(Path1,out_path,"GOD",ob_dict)
remove_ob(Path1,out_path,"PC",ob_dict)
      




   