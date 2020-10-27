import os
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import matplotlib as mp

path0 = "/home/rhuang06/Documents/Annotation_pipeline/"
path = "/home/rhuang06/Documents/Annotation_pipeline/Results/"

def add_chomo():
    go_main_dict = dict()
    GO_folder = os.listdir(path0 + "Proccessed_Data/GO/")
    f = [i for i in GO_folder if "Cow" in i][0]
    go_df = pd.read_csv(path0 + "Proccessed_Data/GO/" + f)
    go_key = list(go_df["Gene stable ID"])
    go_value = list(go_df["Chromosome/scaffold name"])
    go_main_dict.update(dict(zip(go_key,go_value)))
    score_df = pd.read_csv(path + 'GO_score.txt')
    id_list = list(score_df["Cow gene ID"])
    c_list = [go_main_dict.get(i) for i in id_list]
    for num,i in enumerate(c_list):
        if i == None:
            c_list[num] = "None"
    score_df["chromosome"] = c_list
    score_df.to_csv(path + "GO_score_ch.csv", index = None)
    return(score_df)

def make_table_stats(df):
    go_folder = os.listdir(path0 + "Proccessed_Data/GO/")
    file = [i for i in go_folder if "Cow" in i][0]
    go_df = pd.read_csv(path0 + "Proccessed_Data/GO/" + file)
    c_count = go_df["Chromosome/scaffold name"].value_counts()
    c_count = c_count.to_dict()
    chrom_name = [str(i) for i in range(1,30)]
    chrom_name.append("X")
    chrom_name.append("MT")
    #chrom_name.append("None")
    gene_count = list()
    for c in chrom_name:
        try:
            gene_count.append(c_count[c])
        except:
            gene_count.append(0)
    c_count = dict(zip(chrom_name,gene_count))
    c_df = pd.DataFrame(list(c_count.items()), columns = ["chromosome name","total gene count"])
    df_count = df.drop_duplicates(subset = "Cow gene ID")
    df_count_c = df_count["chromosome"].value_counts().to_dict()
    gene_count = list()
    for c in chrom_name:
        try:
            gene_count.append(df_count_c[c])
        except:
            gene_count.append(0)
    c_df["Gene with new GO terms"] = gene_count
    df_count_none = df_count[df_count["have GO terms or not (Yes or None)"] == "None"]
    df_count_none = df_count_none.iloc[:,[0,4]]
    df_count_none = df_count_none["chromosome"].value_counts().to_dict()
    gene_count = list()
    for c in chrom_name:
        try:
            gene_count.append(df_count_none[c])
        except:
            gene_count.append(0)
    c_df["Gene without any GO terms"] = gene_count
    total_list = list(c_df.iloc[:,1::].sum())
    total_list.insert(0,"Total number")
    total_df = pd.DataFrame([total_list], columns= list(c_df.columns.values))
    c_df["Percentage of gene with new GO terms in total"] = (c_df["Gene with new GO terms"]/c_df["total gene count"])*100
    c_df["Percentage of gene without GO terms in total"] = (c_df["Gene without any GO terms"]/c_df["total gene count"])*100
    c_df.append(total_df)
    c_df.to_csv(path + "Chromosome_count.csv", index= None)
    return(c_df)
    



def get_18_cliq():
    gene_name_folder = os.listdir(path0 + "Proccessed_Data/GO/")
    gene_name_dict = dict()
    for gf in gene_name_folder:
        g_file = pd.read_csv(path0 + "Proccessed_Data/GO/" + gf)
        temp_gene_id = list(g_file["Gene stable ID"])
        temp_gene_name = list(g_file["Gene name"])
        temp_gene_dict = dict(zip(temp_gene_id,temp_gene_name))
        gene_name_dict.update(temp_gene_dict)
    gene_name_dict.update({"N/A": "N/A"})    
    clique_df = pd.read_csv(path + "GO_score_with_ani.txt")
    with open(path + "Processed_cliquer_output_dictionary.dat", "rb") as handle:
        clique_file = pickle.load(handle)
    go_main_dict = dict()
    GO_folder = os.listdir(path0 + "Proccessed_Data/GO/")
    f = [i for i in GO_folder if "Cow" in i][0]
    go_df = pd.read_csv(path0 + "Proccessed_Data/GO/" + f)
    go_key = list(go_df["Gene stable ID"])
    go_value = list(go_df["Chromosome/scaffold name"])
    go_main_dict.update(dict(zip(go_key,go_value)))
    id_list = list(clique_df["Cow_gene_ID"])
    c_list = [go_main_dict.get(i) for i in id_list]
    for num,i in enumerate(c_list):
        if i == None:
            c_list[num] = "None"
    clique_df["chromosome"] = c_list
    clique_temp = clique_df[clique_df["chromosome"] == "18"]
    clique_all_id = clique_temp.drop_duplicates(subset = "Cow_gene_ID")
    clique_all_id = list(clique_all_id["Clique_number"])

    clique_temp_id = clique_temp[clique_temp["have_GO_terms"]=="None"]
    clique_temp_id = clique_temp_id.drop_duplicates(subset = "Cow_gene_ID")
    clique_id = clique_temp_id["Clique_number"]
    clique_list = list()
    clique_18_list = list()
    animal_name = ['Gallus_gallus','Bos_taurus','Capra_hircus','Equus_caballus','Homo_sapiens','Mus_musculus','Sus_scrofa','Ovis_aries']
    animal_list = ["ENSGALG","ENSBTA","ENSCHIG","ENSECAG","ENSG","ENSMUSG","ENSSSCG","ENSOARG"]
    animal_index = [4,0,1,2,7,3,5,6]
    for id in clique_all_id: 
        temp_list = clique_file[id]
        for an_num,a_id in enumerate(animal_list):
            if len(temp_list) == 8:
                temp_list.sort()
                temp_list = [temp_list[i] for i in animal_index]
            else:
                if any(i for i in temp_list if a_id in i) is False:
                    temp_list.insert(an_num,"N/A")
        temp_list = [i + "({})".format(gene_name_dict[i]) for i in temp_list]
        clique_list.append(temp_list)
    for cliq_num in clique_id:
        temp_list = clique_file[cliq_num]
        for an_num,a_id in enumerate(animal_list):
            if len(temp_list) == 8:
                temp_list.sort()
                temp_list = [temp_list[i] for i in animal_index]
            else:
                if any(i for i in temp_list if a_id in i) is False:
                    temp_list.insert(an_num,"N/A")
        temp_list = [i + "({})".format(gene_name_dict[i]) for i in temp_list]
        clique_18_list.append(temp_list)
    df_all = pd.DataFrame(clique_list, columns = animal_name)
    df_18 = pd.DataFrame(clique_18_list, columns = animal_name)
    df_all.insert(0,"clique",list(range(1,df_all.shape[0]+1)),True)
    df_18.insert(0,"clique",list(range(1,df_18.shape[0]+1)),True)
    df_all.to_csv(path + "18_chromosome_GO_all_table.txt", sep="\t",index=False)
    df_18.to_csv(path + "18_chromosome_GO_None_table.txt", sep="\t",index=False)
    


    
    



    

    
        
      

    



#make stacking bar graph
score_df = add_chomo()
count_df = make_table_stats(score_df)
get_18_cliq()

plt.rc('text',usetex = True)
plt.rcParams["figure.figsize"] = (22,11)
#plt.rcParams['font.family'] = 'sans-serif'
#plt.rcParams['font.sans-serif'] = 'Calibri'
plt.rcParams.update({'font.size': 15})
indx = count_df["chromosome name"]
all_gene = count_df["total gene count"]
all_new_gene = count_df["Gene with new GO terms"]
none_gene = count_df["Gene without any GO terms"]



plt.bar(indx, none_gene,label = r"Genes without pervious annontation", bottom = all_new_gene + all_gene,color ="#0075f6")
plt.bar(indx, all_new_gene,label = r"Genes with new GO terms", bottom = all_gene, color = "#00bd56")
plt.bar(indx, all_gene, label = r"Total number of genes",color = "#915b4a")


plt.ylabel(r"Number of genes", fontsize=20)
plt.xlabel(r"Chromosome", fontsize=20)
plt.title(r"Number of \textit{Bos taurus} genes with new GO terms per chromosome", fontsize = 25)
plt.legend(bbox_to_anchor = (1.04,0.49), loc = "center left", fontsize = 15)
plt.subplots_adjust(right = 0.75)
plt.savefig(path0 + 'chr.png')
plt.show()


#prepare table for ranking graph
df_new_GO_rank = count_df.loc[:,["chromosome name","Percentage of gene with new GO terms in total","Percentage of gene without GO terms in total"]]
df_no_GO_rank = count_df.loc[:,["chromosome name","Percentage of gene without GO terms in total"]]
df_new_GO_rank["New column"] = df_new_GO_rank["Percentage of gene with new GO terms in total"] - df_new_GO_rank["Percentage of gene without GO terms in total"]

df_new_GO_rank.sort_values(by=["New column"], inplace = True,ascending=False)
df_no_GO_rank.sort_values(by=["Percentage of gene without GO terms in total"], inplace = True,ascending=False)

#make graph of new GO terms-with pervious annotation
plt.rcParams.update({'font.size': 15})
plt.figure(figsize=(26,13))
plt.subplot(1,2,1)

new_chr = df_new_GO_rank["chromosome name"]
new_per = df_new_GO_rank["New column"]


plt.bar(new_chr, new_per, color ="#0075f6")



plt.ylabel(r"Percentage of genes (\%)", fontsize=20)
plt.xlabel(r"Chromosome", fontsize=20)
plt.title(r"Percentage of genes (with previous annotaton) recieving \\ new GO terms in total genes of each chromosome of \textit{Bos taurus} ", fontsize = 20)


#make graph of new GO terms-no pervious annotation
plt.subplot(1,2,2)
no_chr = df_no_GO_rank["chromosome name"]
no_per = df_no_GO_rank["Percentage of gene without GO terms in total"]

plt.bar(no_chr, no_per, color ="#0075f6")



plt.ylabel(r"Percentage of genes (\%)", fontsize=20)
plt.xlabel(r"Chromosome", fontsize=20)
plt.title(r"Percentage of genes (without previous annotation) recieving \\ new GO terms in total genes of each chromosome of \textit{Bos taurus} ", fontsize = 20)
plt.savefig(path0 + 'rank.png')
plt.show()