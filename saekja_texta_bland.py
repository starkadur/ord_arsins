import os
from os import listdir
from os.path import isfile, isdir, join
import json
import pathlib
path2bland = "/home/starkadur/PycharmProjects/RMH/Sofnun_arleg/Samfelagsmidlar/Bland/Skraparar-bland/"
path2textar = "/mnt/gagnageymsla/ordArsins/hreinir/bland/"
years = ['2022','2023']

for year in years:
    path2year = join(path2bland, year)
    path2yearT = join(path2textar, year)

    months = [f for f in listdir(path2year) if isdir(join(path2year, f))]
    textar = []
    for month in months:

        path2month = join(path2year, month)
        path2monthT = join(path2yearT, month)
        days = [f for f in listdir(path2month) if isdir(join(path2month, f))]
        for day in days:
            path2day = join(path2month, day)
            files = [f for f in listdir(path2day) if isfile(join(path2day, f))]
            for file in files:
                path2file = join(path2day, file)
                with open(path2file, "r") as f:
                    data = json.load(f)
                textar = []

                nr = 0
                for item in data['items']:
                    texti = item['text'].strip()
                    file = file.replace(".json","")

                    path2file = join(path2monthT, "{}_{}.txt".format(file, str(nr)))
                    pathlib.Path(path2monthT).mkdir(parents=True, exist_ok=True)
                    with open(path2file, "w")  as f2:
                        f2.write(texti)

                    nr+=1
