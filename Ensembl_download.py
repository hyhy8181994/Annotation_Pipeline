import os
import pandas as pd
from pybiomart import Server
from pybiomart import Dataset
import argparse

ap = argparse.ArgumentParser(description="Download required files from Ensembl database")
ap.add_argument("-outpath",required=False,
	help="Path of directory you want to put output files")

args = vars(ap.parse_args())

out_path=args["outpath"]




out_path = '/home/rhuang06/Documents/Annotation_pipeline/'

if not os.path.exists(out_path + "Data/"):
    os.mkdir(out_path + "Data/")

out_path = out_path + "Data/"

animal_list = ["Cow","Pig","Goat","Sheep","Horse","Human","Mouse","Chicken"]
animal_name_dict = {"Cow": "btaurus_gene_ensembl","Pig": "sscrofa_gene_ensembl","Goat": "chircus_gene_ensembl","Sheep":"oaries_gene_ensembl","Horse":"ecaballus_gene_ensembl","Human":"hsapiens_gene_ensembl","Mouse":"mmusculus_gene_ensembl","Chicken":"ggallus_gene_ensembl"}
list(animal_name_dict.keys())[list(animal_name_dict.values()).index("btaurus" + "_gene_ensembl")]


def biomart(ani_list,ani_dict,out,mode):
    #server = Server(host='http://www.ensembl.org')
    #mart = server['ENSEMBL_MART_ENSEMBL']
    #all_name = mart.list_datasets()
    for animal in ani_list:    
        dataset = Dataset(name= ani_dict[animal],host='http://www.ensembl.org')
        #dataset.list_filters
        #attr_all_list = dataset.attributes()
        if mode == "GO":
            print("Downloading "  + animal + " Gene information")
            if not os.path.exists(out + "/" + "GO"):
                os.mkdir(out + "/" + "GO")
            attr_list = ["ensembl_gene_id","external_gene_name","start_position","end_position","description","transcript_count","chromosome_name"]
            df = dataset.query(attributes= attr_list)
            df.to_csv(out + "/" + "GO" + "/" + animal + "_GO.txt", index = None, header = True)

        elif mode == "GOD":
            print("Downloading " + animal + " Gene Ontology")
            if not os.path.exists(out + "/" + "GOD"):
                os.mkdir(out + "/" + "GOD")
            attr_list = ["ensembl_gene_id","go_id","name_1006","definition_1006"]
            df = dataset.query(attributes= attr_list)
            df.to_csv(out + "/" + "GOD" + "/" + animal + "_GOD.txt",sep='\t', index = None, header = True)
        elif mode == "ORTH":
            print("Downloading " + animal + " Orthologs")
            if not os.path.exists(out + "/" + "ORTH"):
                os.mkdir(out + "/" + "ORTH")
            orth_list = list(ani_dict.keys())
            for o in orth_list:
                if not os.path.exists(out + "/" + "ORTH" + "/" + o):
                    os.mkdir(out + "/" + "ORTH" + "/" + o)
            orth_list.remove(animal)
            sp_list = list()
            for key in orth_list:
                sp_name = ani_dict[key].split("_")[0]
                sp_list.append(sp_name)
            for sp in sp_list:
                attr_list = ["ensembl_gene_id","external_gene_name",sp + "_homolog_ensembl_gene",sp + "_homolog_associated_gene_name",sp + "_homolog_orthology_type"]
                df = dataset.query(attributes= attr_list)
                f = list(animal_name_dict.keys())[list(animal_name_dict.values()).index(sp + "_gene_ensembl")]
                print("Downloading orthologs between " + animal + " and " + f)
                df.to_csv(out + "/" + "ORTH" + "/" + animal + "/" + animal + "_" + f + ".txt", index = None, header = True)             
        elif mode == "PC":
            print("Downloading protein coding genes information for " + animal)
            if not os.path.exists(out + "/" + "PC"):
                os.mkdir(out + "/" + "PC")
            attr_list = ["ensembl_gene_id","external_gene_name","go_id"]
            filter_list = {"biotype": ["protein_coding"]}
            df = dataset.query(attributes= attr_list, filters= filter_list)
            df.to_csv(out + "/" + "PC" + "/" + animal + ".txt", index = None, header = True)            

   



mode_list = ["GO","GOD","ORTH","PC"]

for m in mode_list:
    biomart(animal_name_dict,animal_name_dict,out_path,m)

