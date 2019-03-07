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



#Make new folders for output files
#path1 = path of originial files; path2 = path of directory for new folder
def make_dir(path1,path2):
    Folder =  ["GOD","GO","OMA","ORTH"]    
    if not os.path.exists(path2 + "New"):
        os.mkdir(path2 + "New")
    for i in Folder:
        if not os.path.exists(path2 + "New" + "/" + i):
            os.mkdir(path2 + "New" + "/" + i)
        if i == "ORTH":
            file = os.listdir(path1 + i)
            for animal in file:
                if not os.path.exists(path2 + "New" + "/" + i + "/" + animal):
                    os.mkdir(path2 + "New" + "/" + i + "/" + animal)
        if i == "OMA":
            file1 = os.listdir(path1 + i)
            for animalx in file1:
                if not os.path.exists(path2 + "New" + "/" + i + "/" + animalx):
                    os.mkdir(path2 + "New" + "/" + i + "/" + animalx)
            

#Replace the empty well in data to None
# path = "path of directory with original files"
def get_none(path,out):
    file = os.listdir(path)
    for i in file:
        if i == "ORTH":
            files1 = os.listdir(path + i)
            for name in files1:
                files2 = os.listdir(path + i + "/" + name)
                for name1 in files2:
                    df = pd.read_csv(path + i + "/" + name + "/" + name1)          
                    df1 = df.where((pd.notnull(df)),"None")
                    df1.to_csv(out + "New" + "/" + i + "/" + name + "/" + name1, index = None, header=True)
        if i == "OMA":
            files1 = os.listdir(path + i)
            for name in files1:
                files2 = os.listdir(path + i + "/" + name)
                for name1 in files2:
                    df = pd.read_table(path + i + "/" + name + "/" + name1)          
                    df1 = df.where((pd.notnull(df)),"None")
                    df1.to_csv(out + "New" + "/" + i + "/" + name + "/" + name1, index = None, header=True)
        if i == "GO":        
            files1 = os.listdir(path + i)
            for name in files1:
                df = pd.read_csv(path + i + "/" + name)         
                df1 = df.where((pd.notnull(df)),"None")
                df1.to_csv(out + "New"+ "/" + i + "/" + name, index = None, header=True)
        if i == "GOD":        
            files1 = os.listdir(path + i)
            for name in files1:
                df = pd.read_table(path + i + "/" + name)          
                df1 = df.where((pd.notnull(df)),"None")
                df1.to_csv(out + "New"+ "/" + i + "/" + name, index = None, header=True)




#file = "/home/rhuang06/Documents/Annotation_pipeline/go-basic.obo"
#out_path = "/home/rhuang06/Documents/Annotation_pipeline/"

def obsolete_table (file_path,outfile_path):
    id_GO = []
    id_ob = []
    table = dict()
    n = 0  #counter one for making GO id
    n1 = 0 # counter two for making obsoleted GO term id

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
                        for i in replace_re:
                            t1 = {id4: replace_re}
                            table.update(t1)
                    else:
                        if n2 == 0:
                            no = "None"
                            t2 = {id4: no}
                            table.update(t2)

    df = pd.DataFrame(list(table.items()), columns=["Obsolete GO term", "Replace GO term"])
    df.to_csv(outfile_path + "ob_table.csv", index = None, header=True)

#remove the obsoleted GO id
def remove_ob(p1,p2):
    file = os.listdir(p2 + "New" + "/" + "GOD" + "/")
    OB_table = pd.read_csv(p2 + "ob_table.csv")
    ob_id = OB_table["Obsolete GO term"]
    found_ob_id = []
    counter_one = 0
    for name in file:
        df1 = pd.read_csv(p2 + "New" + "/" + "GOD" + "/" + name)
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
        print(found_ob_id)
        for found_id in found_ob_id:
            row_id = list(df1.loc[df1['GO term accession'] == found_id].index.values)
            replace_id = OB_table[OB_table["Obsolete GO term"] == found_id].iloc[0]["Replace GO term"]
        
            for i in row_id:
                df1.loc[i,'GO term accession']=replace_id
                if replace_id == "None":
                    df1.loc[i,'GO term name']="None"
                    df1.loc[i,'GO term definition']="None"
        df1.to_csv(p2 + "New" + "/" + "GOD" + "/" + name, index = None, header=True)



make_dir(Path1,out_path)

get_none(Path1,out_path)

obsolete_table(file,out_path)

remove_ob(Path1,out_path)

      




   