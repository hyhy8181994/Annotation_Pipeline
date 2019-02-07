import pandas as pd
import numpy
import os

Path1 = "/home/rhuang06/Documents/Annotation_pipeline/New/GO/"
Path2 = "/home/rhuang06/Documents/Annotation_pipeline/Ob_GOterm.csv"


file = os.listdir(Path1)

df2 = pd.read_csv(Path2)
ob_id_1 = df2["Obsolete GO term"]
list1 = []



for name in file:
    df1 = pd.read_csv(Path1 + name)
    na = str(name)
    access_name = df1["GO term accession"]
    print("Accessing" + " " + na)
    list_acc = list(access_name)
    n4 = 0
    n5 = 0
    for i in ob_id_1:
        for a in list_acc:
            if i == a:
                list1.insert(n4,a)
                n4 += 1
            n5 += 1  #row number in GO file 
    for a in list1:
        ob = df1.loc[df1["GO term accession"] == a]
        ob["GO term accession"]

            
        
    



#35473104 row number

         
             
           

        



        
    
    



