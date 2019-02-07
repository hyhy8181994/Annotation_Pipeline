import errno
import pandas as pd
import numpy as np
import os


Path1 = "/home/rhuang06/Documents/Annotation_pipeline/ORTH/"
Path2 = "/home/rhuang06/Documents/Annotation_pipeline/OMA/"


Path3 = "/home/rhuang06/Documents/Annotation_pipeline/New/"

files1 = os.listdir(Path2)

for name in files1:
    try:
        df = pd.read_table(Path2 + name)          
        df1 = df.where((pd.notnull(df)),"None")
        df1.to_csv(Path3 + name, index = None, header=True)
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
