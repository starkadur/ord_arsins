import sys
import os
# add parents directory to path in order for python to find modules located there
sys.path.append(os.path.join(os.path.dirname(__file__), '../ymislegt/db'))
from os import listdir
from os.path import isfile, isdir, join
from lxml import etree
from lxml.etree import Element as ET
import psycopg2
import psycopg2.extras
import re
import configparser


def insert(queries):
    
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'db.ini')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Database config file not found: {config_path}")
    config.read(config_path)

    if 'postgres' not in config:
        raise KeyError("Missing 'postgres' section in DB config")

    cfg = config['postgres']
    host = cfg.get('host', 'localhost')
    database = cfg.get('database')
    user = cfg.get('user')
    password = cfg.get('password')

    if not all([database, user, password]):
        raise ValueError("Database, user and password must be set in the 'postgres' section of the DB config")
    conn = psycopg2.connect(host = host, database=database, user=user, password=password)
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

def get_data(path2year):

    data = {}
    for root, dirs, files in os.walk(path2year, topdown=False):
        for name in files:
            path2file = os.path.join(root, name)
            try:
                tree = etree.parse(path2file, parser)
            except etree.XMLSyntaxError:
                print("Villa við pörsun")
                print(path2file)
                continue

            xml_root = tree.getroot()
            sents = xml_root.findall(".//tei:s", ns)
            for sent in sents:
                words = sent.findall(".//tei:w", ns)
                for word in words:
                    if len(word.attrib['lemma'])>60:
                        continue
                    if word.attrib['lemma'] not in data:
                        data[word.attrib['lemma']] = 0
                    data[word.attrib['lemma']]+=1

    return data


path2folder = "/mnt/gagnageymsla/RMH-2023/TEI/"

corpora= [f for f in listdir(path2folder) if isdir(join(path2folder, f))]


parser = etree.XMLParser(remove_blank_text=True)
ns = {'tei': "http://www.tei-c.org/ns/1.0"}

corpora_done = ["IGC-News1","IGC-News2"]
subcorpora_done = []



for corpus in corpora:
    if corpus in corpora_done:
        print("BÚIÐ")
        print(corpus)
        continue
    
    print(corpus)    
    path2corpus = join(path2folder, corpus)
    
    anas = [f for f in listdir(path2corpus) if isdir(join(path2corpus, f)) and f.endswith(".ana")] 
    if len(anas)!=1:        
        print("Ana-mappa fannst ekki")
        exit()

    
    if corpus.startswith("IGC-PARLA"):
        corpus = corpus.split("/")[0]
        years = [f for f in listdir(path2ana) if isdir(join(path2ana, f))]
        
        for year in years:
            if year not in ['2022','2023']:
                continue
            print(year)
            path2year = join(path2corpus, year)
            data = get_data(path2year)
            insert_data(data, corpus, year)

    elif corpus.startswith("samfelagsmidlar"):

        corpus = "bland"

        years = [f for f in listdir(path2corpus) if isdir(join(path2corpus, f))]
        for year in years:
            if year not in ['2022','2023']:
                continue
            print(year)
            path2year = join(path2corpus, year)
            data = get_data(path2year)
            insert_data(data, corpus, year)
    else:
        print(path2corpus)
        subcorpora = [f for f in listdir(path2corpus) if isdir(join(path2corpus, f))]

        for subcorpus in subcorpora:
            if subcorpus in subcorpora_done:
                print("búið")
                print(subcorpus)
                continue
            print(subcorpus)    
            
            

            path2folder2 = join(path2corpus, subcorpus)
            years = [f for f in listdir(path2folder2) if isdir(join(path2folder2, f))]
            for year in years:
                if year not in ['2022','2023']:
                    continue
                print(year)
                path2year = join(path2folder2, year)
                
                data = get_data(path2year)
                
                queries = []
                insert_data(data, subcorpus, year)
