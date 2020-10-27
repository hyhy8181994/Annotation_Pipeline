import pandas as pd

df = pd.read_csv('/home/rhuang06/Documents/Annotation_pipeline/Results/Chromosome_count.csv')
new_gene = list(df["Gene with new GO terms"])
no_gene = list(df["Gene without any GO terms"])
new_per = list(df["Percentage of gene with new GO terms in total"])
no_per = list(df["Percentage of gene without GO terms in total"])
sec_col = list()
for n,n_p in zip(new_gene,new_per):
    ele_sec_col = "{} ({}{})".format(n,round(n_p,2),"%")
    sec_col.append(ele_sec_col)
df["Gene with new GO terms"] = sec_col
sec_col = list()
for n,n_p in zip(no_gene,no_per):
    ele_sec_col = "{} ({}{})".format(n,round(n_p,2),"%")
    sec_col.append(ele_sec_col)
df["Gene without any GO terms"] = sec_col
df = df.iloc[:,0:4]
df.to_csv('/home/rhuang06/Documents/Annotation_pipeline/Results/Chromosome_count_new.csv',index = None, header = True)
        
    

