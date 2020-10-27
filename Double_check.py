import os
import pandas as pd
from pybiomart import Server
from pybiomart import Dataset
import argparse


path = "/home/rhuang06/Documents/Annotation_pipeline/"

animal_list = ["Cow","Pig","Goat","Sheep","Horse","Human","Mouse","Chicken"]
animal_name_dict = {"Cow": "btaurus_gene_ensembl","Pig": "sscrofa_gene_ensembl","Goat": "chircus_gene_ensembl","Sheep":"oaries_gene_ensembl","Horse":"ecaballus_gene_ensembl","Human":"hsapiens_gene_ensembl","Mouse":"mmusculus_gene_ensembl","Chicken":"ggallus_gene_ensembl"}
#list(animal_name_dict.keys())[list(animal_name_dict.values()).index("btaurus" + "_gene_ensembl")]

if not os.path.exists(path + "temp_Data/"):
    os.mkdir(path + "temp_Data/")


def biomart(ani_list,ani_dict,out,mode):
    #server = Server(host='http://www.ensembl.org')
    #mart = server['ENSEMBL_MART_ENSEMBL']
    #all_name = mart.list_datasets()       
    #attr_all_list = dataset.attributes()
    if mode == "Bos_Chromosome_18":
        dataset = Dataset(name= "btaurus_gene_ensembl",host='http://www.ensembl.org')
        print("Downloading "  + mode + " Gene information")
        if not os.path.exists(path + "temp_Data/" + "Bos_Chromosome_18/"):
            os.mkdir(path + "temp_Data/" + "Bos_Chromosome_18/")
        attr_list = ["ensembl_gene_id"]
        filter_list = {'chromosome_name': ['18']}
        df = dataset.query(attributes= attr_list,filters= filter_list)
        df.to_csv(path + "temp_Data/" + "Bos_Chromosome_18/" + "Cow_C_18.txt", index = None, header = True)
    if mode == "sex":
        for ani in animal_list:
            dataset = Dataset(name= ani_dict[ani],host='http://www.ensembl.org')
            print("Downloading "  + ani + mode + " Gene information")
            if not os.path.exists(path + "temp_Data/" + "sex/"):
                os.mkdir(path + "temp_Data/" + "sex/")
            attr_list = ["ensembl_gene_id"]
            if ani == "Chicken":
                filter_list = {'chromosome_name': ['W',"Z"]}
                df = dataset.query(attributes= attr_list,filters= filter_list)
                df.to_csv(path + "temp_Data/" + "sex/" + ani + "_sex.txt", index = None, header = True)
                print(ani + "W Z")
            else:
                try: 
                    filter_list = {'chromosome_name': ["X"]}
                    df = dataset.query(attributes= attr_list,filters= filter_list)
                    df.to_csv(path + "temp_Data/" + "sex/" + ani + "_sex.txt", index = None, header = True)
                    print(ani + "X Y")
                except:
                    filter_list = {'chromosome_name': ["X"]}
                    df = dataset.query(attributes= attr_list,filters= filter_list)
                    df.to_csv(path + "temp_Data/" + "sex/" + ani + "_sex.txt", index = None, header = True)
                    print(ani + "X")
    if mode == "MT":
        for ani in animal_list:
            dataset = Dataset(name= ani_dict[ani],host='http://www.ensembl.org')
            print("Downloading "  + ani  + mode + " Gene information")
            if not os.path.exists(path + "temp_Data/" + "MT/"):
                os.mkdir(path + "temp_Data/" + "MT/")
            attr_list = ["ensembl_gene_id"]
            try: 
                filter_list = {'chromosome_name': ["MT"]}
                df = dataset.query(attributes= attr_list,filters= filter_list)
                df.to_csv(path + "temp_Data/" + "MT/" + ani + "_MT.txt", index = None, header = True)
            except:
                print("NO Mitochondrial genes in {}".format(ani))




#biomart(animal_list,animal_name_dict,path,"Bos_Chromosome_18")
biomart(animal_list,animal_name_dict,path,"sex")
biomart(animal_list,animal_name_dict,path,"MT")