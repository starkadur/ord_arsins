import os
import re

re_isl_stafir = re.compile(r'[áéíóúýöæþðÁÉÍÓÚÝÆÖÞÐ]')

def er_erlendur(texti):

    m = re_isl_stafir.findall(texti)
    if len(texti)==0:
        return False
    ratio = len(m)/float(len(texti))

    if ratio <0.01:
        return True
    return False

path2folder = "/mnt/gagnageymsla/RMH-2023/markad_2024/2024/"

for root, dirs, files in os.walk(path2folder, topdown=False):
    
    for name in files:
        if not name.endswith(".txt"):
            continue

        if root.find('bland')>-1:
            continue
        if name.endswith("erlent"):
            continue
        path2file = os.path.join(root, name)

        with open(path2file, "r") as f:
            lines = f.readlines()
        
        words = []
        for line in lines:
            if line.strip()!="":
                words.append(line.split("\t")[0])
        text = " ".join(words)
        
        if er_erlendur(text):
            print(path2file)
            new_name = path2file.replace(".txt", ".txt.erlent")
            print(new_name)
            os.rename(path2file, new_name)
