import pandas as pd
import os

path_0 = "/home/rhuang06/Documents/Annotation_pipeline/"
path_1 = path_0 + 'Results/'
path_2 = path_0 + "Proccessed_Data/GOD/"
path_3 = path_0 + "Proccessed_Data/GO/"

def make_table_GO():
    with open(path_1 + "GO_score_ch.csv","r") as s:
        score_dict = dict()
        temp_sub_list = list()
        for num, n_line in enumerate(s):
            if num == 0:
                continue
            #n_line = n_line.strip("\n")            
            temp_score_row = n_line.split(",")
            temp_sub_list.append(temp_score_row[1::])
            try:
                next_n_line = next(s)
                next_temp_score_row = next_n_line.split(",")
                
                if temp_score_row[0] == next_temp_score_row[0]:
                    temp_sub_list.append(next_temp_score_row[1::])
                else:
                    score_dict.update({temp_score_row[0]:temp_sub_list})
                    temp_sub_list = list()
            except:
                pass                             
    go_dict = dict()
    with open(path_0 + "go-basic.obo","r") as g:
        #go_basic_raw = g.readlines()
        for line in g:
            if "[Term]" in line:
                temp_id = next(g)
                temp_id = temp_id.strip("\n")
                temp_id = temp_id.split(" ")[1]
                temp_name = next(g,2)
                temp_name = temp_name.strip("\n")
                temp_name = temp_name.replace("name: ","")
                temp_name = temp_name.replace(" ","_")
                temp_type = next(g,3)
                temp_type = temp_type.strip("\n")
                temp_type = temp_type.replace("namespace: ","")
                if "obsolete" in temp_name:
                    continue
                temp_complex = [temp_name,temp_type]
                temp_dict = {temp_id:temp_complex}
                go_dict.update(temp_dict)
    go_score_df = pd.read_csv(path_1 + "GO_score_ch.csv")
    go_score_df_f_3 = go_score_df.iloc[:,[0,1,2]]
    gene_table = pd.read_csv(path_3 + "Cow_GO.txt")
    go_term_table = pd.read_csv(path_2 + "Cow_GOD.txt")
    
    go_term_table = go_term_table[go_term_table["Gene stable ID"].str.contains("ENSBTAG")]
    
    
    go_score_df_f_3 = go_score_df_f_3.rename(columns = {"Cow gene ID":"Gene stable ID","Suggested GO term ID": "GO term accession"})
    go_term_table_s_2 = go_term_table.loc[:,["Gene stable ID","GO term accession"]]
    gene_table_s_3 = gene_table.loc[:,["Gene stable ID","Gene name","Chromosome/scaffold name"]]
    gene_name_dict = dict(zip(gene_table_s_3["Gene stable ID"],gene_table_s_3["Gene name"]))
    gene_chr_dict = dict(zip(gene_table_s_3["Gene stable ID"],gene_table_s_3["Chromosome/scaffold name"]))
    
    go_dec_temp = list(go_score_df["have GO terms or not (Yes or None)"])
    go_cat_temp_2 = list()
    for dec in go_dec_temp:
        if dec == "None":
            go_cat_temp_2.append("New(no_previous_annotation)")
        else:
            go_cat_temp_2.append("New")
    go_term_table_s_2["Score"] = ["None"]*go_term_table_s_2.shape[0]
    go_term_ac = list(go_term_table["GO term accession"])
    go_cat_temp_1 = list()
    for ac in go_term_ac:
        if ac == "None":
            go_cat_temp_1.append(ac)
        else:
            go_cat_temp_1.append("Existing")
    
    go_term_table_s_2["GO term category"] = go_cat_temp_1
    go_score_df_f_3["GO term category"] = go_cat_temp_2
    go_term_table_s_2 = go_term_table_s_2.append(go_score_df_f_3,sort = True)
    go_term_table_s_2.sort_values(by = "Gene stable ID", inplace = True)
    output_file = open(path_0 + "Result_file.txt","w+")
    output_file.write("Ensemble_gene_id\tGene_name\tChromosome\tGO_term\tGO_term_type\tGO_term_name\tGO_term_category\tGO_term_score\n")
    #output_file.close()
    #output_file = open(path_0 + "Result_file.txt","a")
    for index, row in go_term_table_s_2.iterrows():
        row = list(row)
        gene_id = row[2]
        if "ENS" in gene_id:
            if row[0] == "None":
                go_id = row[0]
                gene_name = gene_name_dict[gene_id]
                gene_chr = gene_chr_dict[gene_id]
                go_name = "None"
                go_type = "None"
            else:
                go_id = row[0]
                gene_name = gene_name_dict[gene_id]
                gene_chr = gene_chr_dict[gene_id]
                try:
                    go_name = go_dict[go_id][0]
                    go_type = go_dict[go_id][1]
                    go_name.replace(",","_")
                    go_name.replace(" ","_")
                    #None
                except:
                    go_name = "None"
                    go_type = "None"
        new_line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(row[2],gene_name,gene_chr,row[0],go_type,go_name,row[1],row[3])
        output_file.write(new_line)
    output_file.close()

#make_table_GO()
table_df = pd.read_table(path_0 + "Result_file.txt")
table_df = table_df.drop_duplicates()
table_df = table_df[table_df["GO_term"] != "None"]
table_df.to_csv(path_0 + "Result_file.txt",sep="\t",index=None,header=True)
