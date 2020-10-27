import pickle
import random
import os

folder = ["size_5","size_10","size_50","size_100","size_500","size_1000"]
path = "/home/rhuang06/Documents/Annotation_pipeline/Results/"
path1 = path + "test/"


for f in folder:
    if not os.path.exists(path + f):
        os.mkdir(path + f) 


with open(path + '/size8.txt', "r") as handle:
        a = handle.readlines()



for i in range(10):
    x = random.choices(list(a),k=5)
    cliq_dict = dict(zip(list(range(len(x))),x))
    with open(path1 + "/size_5/example_" + str(i) + ".txt","w") as handle:
        for ii in x:
                handle.writelines(ii)

for i in range(10):
    x = random.choices(list(a),k=10)
    cliq_dict = dict(zip(list(range(len(x))),x))
    with open(path1 + "/size_10/example_" + str(i) + ".txt","w") as handle:
        for ii in x:
                handle.writelines(ii)

for i in range(10):
    x = random.choices(list(a),k=50)
    with open(path1 + "/test/size_50/example_" + str(i) + ".txt","w") as handle:
        for ii in x:
                handle.writelines(ii)

for i in range(10):
    x = random.choices(list(a),k=100)
    cliq_dict = dict(zip(list(range(len(x))),x))
    with open(path1 + "/test/size_100/example_" + str(i) + ".txt","w") as handle:
        for ii in x:
                handle.writelines(ii)

for i in range(10):
    x = random.choices(list(a),k=500)
    cliq_dict = dict(zip(list(range(len(x))),x))
    with open(path1 + "/test/size_500/example_" + str(i) + ".txt","w") as handle:
        for ii in x:
                handle.writelines(ii)

for i in range(10):
    x = random.choices(list(a),k=1000)
    cliq_dict = dict(zip(list(range(len(x))),x))
    with open(path1 + "/size_1000/example_" + str(i) + ".txt","w") as handle:
        for ii in x:
                handle.writelines(ii)