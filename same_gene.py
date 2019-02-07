import pandas as pd
import numpy as num
import os

Path1 = "/home/rhuang06/Documents/Annotation_pipeline/New_ORTH/"

folder = os.listdir(Path1)

def eq(x,y):
    n = 0
    n5 = 0
    for i in range(len(x)):
        if x[n] == "NONE" or y[n] == "NONE":
            n += 1
        elif "Mouse" or "Human" in name:
            if y[n].find(x[n]) == -1:
                print(x[n])
                print(y[n])
                n += 1
                n5 += 1
        else:
            if x[n] != y[n]:
                n5 += 1
                if n5 == 1:
                   print("Find different " + "name") 
                print(x[n])
                print(y[n])
                n += 1
                
    if n5 == 0:
        print("All orthologous gene name is same in " + name)

            


for folder_name in folder:
    file = os.listdir(Path1 + folder_name)
    for name in file:
        df = pd.read_csv(Path1 + folder_name + "/" +name)
        df1 = df.where((pd.notnull(df)),"None")
        gene_name = df1["Gene name"]
        name_1 = name.strip(folder_name)
        name_2 = name_1.strip("_")
        name_3 = name_2.strip("txt")
        name_4 = name_3.strip(".")
        other_name = df1[name_4 + " " + "gene name"]
        gene_name_1 = gene_name.str.upper()
        other_name_1 = other_name.str.upper()
        gene_name_new = gene_name_1[gene_name_1 != "None"]
        other_name_new = other_name_1[other_name_1 != "None"]
        if folder_name == "Human":
            n1 = 0
            n3 = 0
            for i in range(len(gene_name_new)):
                if gene_name_new[n1] == "NONE" or other_name_new[n1] == "NONE":
                    n1 += 1
                else:
                    if gene_name_new[n1].find(other_name_new[n1]) == -1:
                        n3 += 1
                        if n3 == 1:
                            print("Find different " + "name")
                        print(gene_name_new[n1])
                        print(other_name_new[n1])
                        n1 += 1
                        
            if n3 == 0:
                print("All orthologous gene name is same in " + name)
        if folder_name == "Mouse":
            n2 = 0
            n4 = 0
            for i in range(len(gene_name_new)):
                if gene_name_new[n2] == "NONE" or other_name_new[n2] == "NONE":
                    n2 += 1
                else:
                    if gene_name_new[n2].find(other_name_new[n2]) == -1:
                        n4 += 1
                        if n4 == 1:
                            print("Find different " + "name")
                        print(gene_name_new[n2])
                        print(other_name_new[n2])
                        n2 += 1
                        
            if n4 == 0:
                print("All orthologous gene name is same in " + name)

        else:
            eq(gene_name_new,other_name_new)
             
                    

            
        
        

                        

        
        
        

    
            

