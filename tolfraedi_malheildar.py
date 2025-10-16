import sys
import os
# add parents directory to path in order for python to find modules located there
sys.path.append(os.path.join(os.path.dirname(__file__), '../ymislegt/db'))
from os import listdir
from os.path import isfile, isdir, join
import re



def insert_data(data, corpus, year):

    queries = []
    for lemma in data:
        queries.append([lemma, data[lemma], corpus, year])
        if len(queries)>7000:
            insert(queries)
            queries = []
        insert(queries)
        queries = []
    insert(queries)

def cnt_data(path2year):

    cnt_ = 0


    for root, dirs, files in os.walk(path2year, topdown=False):
        for name in files:
            path2file = os.path.join(root, name)
            with open(path2file, "r") as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if line!="":
                    splt = line.split("\t")
                    if len(splt[2])>60:
                        continue
                    if not splt[1].startswith("p"):
                        cnt_+=1


    return cnt_


path2folder = "/mnt/gagnageymsla/19aldar/markad/"

timaritin = [f for f in os.listdir(path2folder) if os.path.isdir(os.path.join(path2folder, f))]
cnt = {}
for timarit  in timaritin:
    print(timarit)
    path2timarit = os.path.join(path2folder, timarit)
    years = [f for f in os.listdir(path2timarit) if os.path.isdir(os.path.join(path2timarit, f))]
    for year in years:
        if year not in cnt:
            cnt[year] = 0
        path2year = os.path.join(path2timarit, year)


        cnt[year] += cnt_data(path2year)

for year in cnt:
    print("{}\t{}\n".format(year, cnt[year]))
