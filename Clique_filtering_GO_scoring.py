import os
import time
import pandas as pd
import multiprocessing as mp
import pickle
import shutil
import argparse

# parsing the arguments and warning message
ap = argparse.ArgumentParser(description="Filter cliques and GO term scoring")
ap.add_argument("-path",required=False,
	help="Path of Result folder")
ap.add_argument("-outpath",required=False,
	help="Path of directory you want to put output file")

args = vars(ap.parse_args())


path=args["path"]
path1=args["outpath"]


path = "/home/rhuang06/Documents/Annotation_pipeline/Results/"
path1 = '/home/rhuang06/Documents/Annotation_pipeline/'



start = time.time()
#load original cliquer outout file and made to a dictionary for later removal process
#key = 'size'_'number' e.g. 7_1: clique size 7, number 1
#value = clique 
def load_cfile(input_file):
    with open(input_file, "r") as file:
        lines = file.readlines()
        clique_1 = list()
        size_list = list()
        for number,line in enumerate(lines):
            temp_cliq = line.split(":")[1]
            temp_cliq = temp_cliq.strip("\n").split(" ")
            temp_cliq = list(filter(None, temp_cliq))       # Remove extra strings and save cliques in list
            size = str(len(temp_cliq)) + "_" + str(number)  # Size information
            clique_1.append(temp_cliq)
            size_list.append(size)
        clique_1_dict = dict(zip(size_list,clique_1))
    return(clique_1_dict)



 
#Get absolute path of clique output files
def load_sep_file(Path):
    files = os.listdir(Path)
    files.sort()
    abs_list = list()
    for f in files :
        abs_file = Path + f
        abs_list.append(abs_file)
    return(abs_list)


#"repeated" cliques are defined as small size clique that included in one bigger sized clique
#Function to remove "repeated" cliques based on size 8 cliques, temp files are saved in temp_result
def main_frame_7(num):
    clique_1 = load_cfile(path + "size8.txt")
    abs_list = load_sep_file(path + "sep_size/")
    def remove(n,abs):     
        print("process " + os.path.basename(abs[n]))
        file_name = os.path.basename(abs[n])
        clique_2 = load_cfile(abs[n]) 
        cliq_dict = clique_2
        remove_index = list()             
        for value in clique_1.values():   
            for ne,elem in clique_2.items():        
                dec = all(x in value for x in elem)                
                if dec is True:
                    remove_index.append(ne)
        for ri in remove_index:
            cliq_dict.pop(ri,None)
        print(os.path.basename(abs[num]) + " process finished")        
        with open(path + "temp_result/{}.dat".format(file_name),"wb") as handle:
            pickle.dump(cliq_dict,handle,protocol=pickle.HIGHEST_PROTOCOL)
    remove(num,abs_list)

#Load big cliques for removing process and move them to processed_file folder
def load_and_move(c_size):
    #Load cliques to main_dict
    main_dict = dict()    
    proced_files = list()
    number = int(c_size.split("_")[0])
    changed_number = str(number + 1) + "_"
    #Make directory for processed files  
    if not os.path.exists(path + "{}temp_results/".format(c_size)):
        os.mkdir(path + "{}temp_results/".format(c_size))
    if not os.path.exists(path + "processed_temp_results/"):
        os.mkdir(path + "processed_temp_results/")
    if  c_size == "7_":
        temp_files = os.listdir(path + "temp_result/")
        for temp_f in temp_files:
            if c_size in temp_f:
                proced_files.append(temp_f)
                with open(path + "temp_result/" + temp_f,"rb") as temp_handle:
                    temp_dict = pickle.load(temp_handle)
                    main_dict.update(temp_dict)
        for p_f in proced_files:
            shutil.move(path + "temp_result/" + p_f,path + "processed_temp_results/" + p_f) 
    else:
        temp_files = os.listdir(path + "{}temp_results/".format(changed_number))
        for temp_f in temp_files:
            if c_size in temp_f:
                proced_files.append(temp_f)
                with open(path + "{}temp_results/".format(changed_number) + temp_f,"rb") as temp_handle:
                    temp_dict = pickle.load(temp_handle)
                    main_dict.update(temp_dict)
        #Move files to processed folder
        for p_f in proced_files:
            shutil.move(path + "{}temp_results/".format(changed_number) + p_f,path + "processed_temp_results/" + p_f)
    return(main_dict)


#Function to remove "repeated" cliques based on size 7, 6, 5, 4 cliques, temp files are saved in 7_temp_result,6_temp_result, 5_temp_result and 4_temp_result
def main_frame_6(num):   
    clique_1 = seven_dict
    existed_files = os.listdir(path + "processed_temp_results/")
    size_list = ["7_","6_","5_","4_"]
    temp_size_list = list()
    for s in size_list:
        if any(i for i in existed_files if s in i) is True:
            temp_size_list.append(s)
    #temp_size_list.sort()
    #print(temp_size_list)
    decision = temp_size_list[-1]
    if decision == "7_":
        abs_list = load_sep_file(path + "temp_result/")
    else:
        change_n = str(int(decision.split("_")[0])+1) + "_"
        abs_list = load_sep_file(path + "{}temp_results/".format(change_n))
    def remove(n,abs,dec):     
        print("process " + os.path.basename(abs[n]))
        file_name = os.path.basename(abs[n])
        with open(abs[n],"rb") as handle:
            clique_2 = pickle.load(handle) 
            cliq_dict = clique_2
        remove_index = list()    
        for value in clique_1.values():   
            for ne,elem in clique_2.items():        
                dec = all(x in value for x in elem)                
                if dec is True:
                    remove_index.append(ne)
                    #cliq_dict.pop(ne,None)
        for ri in remove_index:
            cliq_dict.pop(ri,None)  
        print(os.path.basename(abs[num]) + " process finished")        
        with open(path + "{}temp_results/{}".format(decision,file_name),"wb") as handle:
            pickle.dump(cliq_dict,handle,protocol=pickle.HIGHEST_PROTOCOL)
    remove(num,abs_list,decision)


#Processed files are saved in processed_temp_file

#Preprocessing cliques, remove cliques that does not contain cow and put cow in the first position of each clique
def preprocess(input_file,index):
    temp_cliq = input_file
    clique_1 = list()
    size_list = list()          
    #dec = None
    for key, value in temp_cliq.items():  
        id_list = list() 
        for num in value: 
            g_id = index_df[int(num)]   # translate clique number to gene stable ID
            if "ENSBTAG" in g_id:
                id_list.insert(0,g_id)  # make sure cow gene id in first position of list
                #dec = "Yes"
            else:
                id_list.append(g_id)
        if any(i for i in id_list if "ENSBTAG" in i) is True:                # cliques without cow are not saved
            clique_1.append(id_list)
            size_list.append(key)
        else:
            pass                 
    clique_1_dict = dict(zip(size_list,clique_1))
    print("\nPreprocessing of cliques is finished\n")
    print("Result {} cliques\n".format(len(clique_1_dict.values())))
    return(clique_1_dict)



#Score function main frame
def score_main(input_dict,cow_list,cow_id_list,id):
    score_dict = {"ENSGALG": 3, "ENSMUSG": 2, "ENSSSCG": 2, "ENSECAG": 2, "ENSG": 2, "ENSOARG": 1, "ENSCHIG": 1}
    #go_values = list(input_dict.values())
    #go_keys = list(input_dict.keys())
    temp_list = list()
    anim_list = list()
    time_file = open(path + "GO_score.txt","a+")
    time_file_se = open(path + "GO_score_with_ani.txt","a+")
    for gk, gv in input_dict.items():
        #print(gv)
        edited_gv = [i for i in gv if any(i in ii for ii in cow_list) is False] # remove go terms that appears in cow's gene        
        if len(edited_gv) != 0:
            anim_list.append(gk)
        if any("None" in i for i in gv) is True:
            try:
                edited_gv.remove("None") # remove None term
            except:
                pass
        temp_list.append(edited_gv)
    temp_list = list(filter(None,temp_list))# remove empty value in dictionary
    temp_dict = dict(zip(anim_list,temp_list))
    proce_id = list()
    for key_1, value_1 in temp_dict.items():
        for vv in value_1:                
            animal_list = list(temp_dict.keys())                 
            animal_name = list()
            if any(vv in i for i in proce_id) is True:
                continue
            else:
                if animal_list == 1:
                    sp_id = key_1.split("0")[0]
                    score_list = [1/score_dict.get(sp_id)]
                    animal_name.append(key_1)
                else:
                    animal_list.remove(key_1)
                    score_list = list()
                    sp_id = key_1.split("0")[0]
                    sp_score = 1/score_dict.get(sp_id)
                    score_list.append(sp_score)
                    animal_name.append(key_1)
                    for aa in animal_list:
                        sub_go_list = temp_dict.get(aa)
                        if any(vv in i for i in sub_go_list) is True:
                            sp_id = aa.split("0")[0]
                            sp_score = 1/score_dict.get(sp_id)
                            score_list.append(sp_score)
                            proce_id.append(vv)
                            animal_name.append(key_1)
            #print(cow_id_list)
            if (len(cow_list) == 1) & (cow_list[0] == "None"):
                cow_dec = "None"
            else:
                cow_dec = "Yes"          
            output_line = "{},{},{},{}\n".format(cow_id_list,vv,sum(score_list),cow_dec)
            temp_sec = ' '.join(animal_name)
            output_line_sec = "{},{},{},{},{}\n".format(cow_id_list,vv,temp_sec,id,cow_dec)
            time_file.write(output_line)
            time_file_se.write(output_line_sec)
    time_file.close()
    time_file_se.close()

                       
                              


#translate index number in to gene id and then GO term id
#and the score of each GO id will be calculate
def translate(input_dict):
    #file = os.listdir(path)  
    temp_file = input_dict
    #print(temp_file)
    #cliq_list = list(temp_file.values())
    time_file = open(path + "GO_score.txt","w+")
    time_file_se = open(path + "GO_score_with_ani.txt","w+")
    time_file.write("Cow gene ID,Suggested GO term ID,Score,have GO terms or not (Yes or None)\n")
    time_file_se.write("Cow_gene_ID,Suggested_GO_term,Animial_gene_ID,Clique_number,have_GO_terms\n")
    time_file.close()
    time_file_se.close()
    start_time = time.time()
    for c_index, c in temp_file.items():
        cow_id = c[0]
        cow_go = fuse_df[c[0]]
        c.remove(cow_id)
        GO_l = [fuse_df[id] for id in c]
        temp_cliq = dict(zip(c,GO_l))           
        score_main(temp_cliq,cow_go,cow_id,c_index)
        end = time.time() - start_time
    print("Scoring cost " + str(end) + "sec")

# produce statisitcs information of output results
def load_resuts():
    df = pd.read_csv(path + "GO_score.txt")
    df = df.sort_values("Cow gene ID").drop_duplicates(subset = ["Cow gene ID", "Suggested GO term ID"], keep ="last")
    num = df["Cow gene ID"].drop_duplicates()
    n_df = df[df["have GO terms or not (Yes or None)"] == "None"]
    nn_df = n_df["Cow gene ID"].drop_duplicates()
    print("total number of cow genes getting new GO terms")
    print(num.shape[0])
    print("number of cow genes without any GO terms geting new GO terms")
    print(nn_df.shape[0])
    print("number of new GO terms found for cow genes without GO terms")
    print(n_df.shape[0])
    print("total number of new GO terms")
    print(df.shape[0])

def remove_temp(path):
    if os.path.exists(path) is True:
        shutil.rmtree(path)

#load GO term library
def load_go():
    print("Preparing GO term library")
    GO_files = os.listdir(path1 + "/Proccessed_Data/GOD/")
    fuse_df = pd.DataFrame()
    for GO_file in GO_files:
        df = pd.read_csv(path1 + "/Proccessed_Data/GOD/" + GO_file)
        df = df.loc[:,["Gene stable ID","GO term accession"]]
        fuse_df = fuse_df.append(df)
    #fuse_df.sort_values(by=["GO term accession"], inplace = True)
    fuse_df.to_csv(path1 + "/Proccessed_Data/Fuse_Orth_file/GO_fuse_file.csv", index= None, header= False)
    print("GO term library preparation finished\n")

    print("Save GO fuse file to dictionary")
    with open(path1 + "/Proccessed_Data/Fuse_Orth_file/GO_fuse_file.csv","r") as file:
        go_fuse = file.readlines()
    for num_line,go_line in enumerate(go_fuse):
        if "ENS" not in go_line:
            pass
        else:
            go_fuse = go_line.strip("\n")
            go_fuse = go_fuse.split(",")
            if num_line == 0: 
                main_go_dict = {go_fuse[0]:[go_fuse[1]]}
            else: 
                try:
                    go_get = main_go_dict[go_fuse[0]]
                    if go_fuse[1] != "None":
                        go_get.append(go_fuse[1])
                        main_go_dict.update({go_fuse[0]:go_get})
                except:
                    main_go_dict.update({go_fuse[0]:[go_fuse[1]]})
    return(main_go_dict)

def double_check():
    go_df = pd.read_csv(path + "GO_score.txt")
    go_df = go_df[go_df["Suggested GO term ID"] != "None"]
    
    go_df = go_df[go_df["Cow gene ID"].str.contains("BTAG")]
    go_df.to_csv(path + "GO_score.txt",index = None, header = True)


#Filter "repeated" cliques based on size
s = time.time()
#set up multipleprocessing and process files   
sep_length = len(os.listdir(path + "sep_size/"))

if not os.path.exists(path + "temp_result/"):
    os.mkdir(path + "temp_result/")

pool = mp.Pool(processes = 6)
pool.map(main_frame_7, range(sep_length))

try:
    seven_dict = load_and_move("7_")
except:
    pass
#print("cost{} sec".format(time.time()-s))

#Filter "repeated" cliques based on size 7, size 6, size 5 and size 4
for c_folder in ["7_","6_","5_","4_"]:
    s = time.time()
    if c_folder == "7_":
        folder_length = len(os.listdir(path + "temp_result/"))
    else:
        x = str(int(c_folder.split("_")[0])+1) + "_"
        folder_length = len(os.listdir(path + "{}temp_results/".format(x)))
    print(folder_length)
    pool = mp.Pool(processes = 6)
    pool.map(main_frame_6, range(folder_length))
    minus_one = str(int(c_folder.split("_")[0])-1) + "_"
    if c_folder == "4_":
        pass
    else:
        seven_dict = load_and_move(minus_one)
    print("cost{} sec".format(time.time()-s))


filter_end = time.time() -start
print("Filtering process cost {} mins".format((filter_end)/60))

#Load saved files and combined into one dictionary

for tf in os.listdir(path + "4_temp_results/"):
    shutil.move(path + "4_temp_results/" + tf, path + "processed_temp_results/" + tf)
main_dict = dict()
for ss in os.listdir(path + "processed_temp_results/"):
    with open(path + "processed_temp_results/" + ss, "rb") as hh:
        hh_t = pickle.load(hh)        
        main_dict.update(hh_t)

t_s_8 = load_cfile(path + "size8.txt")
main_dict.update(t_s_8)

def output_main():
    with open(path + "Processed_cliquer_output.txt","w") as h:
        for key, value in main_dict.items():
            size = key.split("_")[0]
            forward = "size={}, weight={}:   ".format(size,size)
            backward = str(value).strip("[]")
            backward = backward.replace("'","")
            backward = backward.replace(",","")
            backward = backward + "\n"
            all = forward + backward
            h.write(all)
    with open(path + "Processed_cliquer_output_dictionary.dat","wb") as handle:
        pickle.dump(main_dict,handle,protocol=pickle.HIGHEST_PROTOCOL)


    
      
#extract the clique with Bos with "None" in GO ID 
index_df = pd.read_csv(path1 + 'Proccessed_Data/Fuse_Orth_file/' + "Cliquer_index_one_file.csv")          
index_key,index_value = list(index_df["Gene stable ID"]),list(index_df["Number"])
index_df = dict(zip(index_value,index_key))
fuse_df = load_go()
main_dict = preprocess(main_dict,index_df)

output_main()
translate(main_dict)
double_check()
load_resuts()
folder_need_remove = ["temp_result","4_temp_results","5_temp_results","6_temp_results","7_temp_results","sep_size"]
for folder in folder_need_remove:
    remove_temp(path + folder)
try:
    os.remove(path + "size7.txt")
    os.remove(path + "size8.txt")
except:
    pass