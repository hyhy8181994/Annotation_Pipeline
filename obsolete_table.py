import re
import pandas as pd

file = "/home/rhuang06/Documents/Annotation_pipeline/go-basic.obo"

id_GO = []
id_ob = []
table = dict()
n = 0
n1 = 0
n2 = 0
n3 = 1

with open(file, "r") as f:
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
                n += 1                                   
        if "is_obsolete: true" in line:
            id4 = id_GO[n-1]
            id_ob.insert(n1, id4)
            n1 += 1
            replace = []
            n2 = 0
            for x in range(6):
                next_line = next(f)
                if "consider:" in next_line:
                    replace.insert(n2,next_line)
                    n2 += 1
                    n3 = 0
                    replace_re = []
                    for i in replace:
                        a = i.strip("\n")
                        b = a.strip("consider: ")
                        replace_re.insert(n3,b)
                        n3 += 1
                    for i in replace_re:
                        t1 = {id4 : replace_re}
                        table.update(t1)
                else:
                    if n2 == 0:
                        no = "None"
                        t2 = {id4 : no}
                        table.update(t2)


df = pd.DataFrame(list(table.items()), columns = ["Obsolete GO term","Replace GO term"])

df.to_csv("/home/rhuang06/Documents/Annotation_pipeline/Ob_GOterm.csv", index = None, header=True)

#df2 = pd.read_csv("/home/rhuang06/Documents/Annotation_pipeline/Ob_GOterm.csv")

###################Next step

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
        re_term = df.loc[df["GO term accession"] == a]["Replace GO term"]
        df1.loc[df1["GO term accession"] == a]["GO term accession"]
        #ob["GO term accession"]


      




   