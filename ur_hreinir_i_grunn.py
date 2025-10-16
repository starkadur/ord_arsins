import sys
import os
# add parents directory to path in order for python to find modules located there
sys.path.append(os.path.join(os.path.dirname(__file__), '../ymislegt/db'))
from os import listdir
from os.path import isfile, isdir, join
import psycopg2
import psycopg2.extras
import re

def insert(queries):
    
    conn = psycopg2.connect(host = 'localhost', database='ord_arsins', user='starkadur', password='1plus1er1')
    dbString = "insert into ord_arsins_lemmur (lemma, fjoldi, midill, artal) VALUES(%s, %s, %s, %s)"
    cur = conn.cursor()

    for q in queries:
        cur.execute(dbString, q)

    conn.commit()
    cur.close()
    conn.close()

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

def get_data(path2year):

    data = {}
    for root, dirs, files in os.walk(path2year, topdown=False):
        for name in files:
            if name.endswith(".erlent"):
                continue
            path2file = os.path.join(root, name)
            with open(path2file,"r") as f:
                lines = f.readlines()
            for line in lines:
                if line.strip()=="":
                    continue
                splt = line.strip().split("\t")
                lemma = splt[2]
                if len(lemma)>60:
                    continue
                if lemma not in data:
                    data[lemma] = 0
                data[lemma]+=1

    return data


path2folder = "/mnt/gagnageymsla/RMH-2023/markad_2024/2024"

corpora = [f for f in listdir(path2folder) if isdir(join(path2folder, f))] 

corpora_done = ["althingi","andriki","bb","bbl","bondi","deiglan","dfs","domstolar","dv_is"]




for corpus in corpora:
    if corpus.startswith("althingis"):
        continue
    if corpus in corpora_done:
        continue 

    print("######## {} #########".format(corpus))
    
    path2corpus = join(path2folder, corpus)

   
    corpus = corpus.split("/")[0]
    years = [f for f in listdir(path2corpus) if isdir(join(path2corpus, f))]
    for year in years:
        if year not in ['2024']:
            continue
        print(year)
        
        path2year = join(path2corpus, year)
        data = get_data(path2year)
        insert_data(data, corpus, year)

    '''elif corpus.startswith("samfelagsmidlar"):

        corpus = "bland"

        years = [f for f in listdir(path2corpus) if isdir(join(path2corpus, f))]
        for year in years:
            if year not in ['2024']:
                continue
           
            path2year = join(path2corpus, year)
            data = get_data(path2year)
            insert_data(data, corpus, year)
    else:

        
        years = [f for f in listdir(path2folder2) if isdir(join(path2folder2, f))]
        for year in years:
            if year not in ['2024']:
                continue
            print(year)
            path2year = join(path2folder2, year)
            print(path2year)
            exit()
            data = get_data(path2year)

            queries = []
            insert_data(data, subcorpus, year)'''
