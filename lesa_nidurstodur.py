
import psycopg2
import psycopg2.extras
import sys
import os
import operator
import re

YEAR = '2024'
LAST_YEAR = "2023"
re_tala = re.compile(r'\d+[\.\%\,\d]*')
re_oord = re.compile(r'^[^a-zA-ZáéíóúýæöðþÁÉÍÓÚÝÆÞÐÖ]+$')
conn = psycopg2.connect(host = 'localhost', database='ord_arsins', user='starkadur', password='1plus1er1')
data_curryear = {}
dbString = "select * from ord_arsins_lemmur where artal = '{}'".format(YEAR)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute(dbString)
rows = cur.fetchall()
cur.close()

for row in rows:

    lemma = row['lemma'].lower()
    if re_tala.match(lemma) or re_oord.match(lemma):
        continue
    fjoldi = row['fjoldi']

    if lemma not in data_curryear:
        data_curryear[lemma] = 0
    data_curryear[lemma]+=fjoldi

data_eldra = {}
dbString = "select * from ord_arsins_lemmur where artal < %s"
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute(dbString, [YEAR])
rows = cur.fetchall()
cur.close()

for row in rows:

    lemma = row['lemma'].lower()
    if re_tala.match(lemma) or re_oord.match(lemma):
        continue

    fjoldi = row['fjoldi']

    if lemma not in data_eldra:
        data_eldra[lemma] = 0
    data_eldra[lemma]+=fjoldi


data_lastyear= {}
dbString = "select * from ord_arsins_lemmur where artal = %s and midill != 'domstolar'"
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute(dbString, [LAST_YEAR])
rows = cur.fetchall()
cur.close()
conn.close()

for row in rows:

    lemma = row['lemma'].lower()
    if re_tala.match(lemma) or re_oord.match(lemma):
        continue

    fjoldi = row['fjoldi']

    if lemma not in data_lastyear:
        data_lastyear[lemma] = 0
    data_lastyear[lemma]+=fjoldi


#lista orð sem birtast á liðnu ári en aldrei árin á undan
data = {}
for lemma in data_curryear:
    if lemma.startswith("-"):
        continue
    

    if lemma not in data_eldra:
        data[lemma] = data_curryear[lemma]



data_sorted = sorted(data.items(), key=operator.itemgetter(1))
with open("nidurstodur/nytt_ord.txt","w") as f:
    for i in reversed(range(0,len(data_sorted))):

        f.write("{}\t{}\n".format(data_sorted[i][0], data_sorted[i][1]))

#list yfir orð sem birtust tvöfalt oftar á liðnu ári en öll fyrri ár til samans
data = {}
for lemma in data_curryear:
    if lemma in data_eldra:
        if data_curryear[lemma] >= 2*data_eldra[lemma]:
            data[lemma] = data_curryear[lemma]

data_sorted = sorted(data.items(), key=operator.itemgetter(1))
with open("nidurstodur/tvofalt_oftar.txt","w") as f:
    for i in reversed(range(0,len(data_sorted))):

        f.write("{}\t{}\t{}\n".format(data_sorted[i][0], data_sorted[i][1], data_eldra[data_sorted[i][0]]))

#list yfir orð sem birtust að lágmarki sex sinnum á nýju ári en sjaldnar öll önnur ár
data = {}
for lemma in data_curryear:
    if data_curryear[lemma]>=6:
        if lemma in data_eldra:
            if data_eldra[lemma] < 6:
                data[lemma] = data_curryear[lemma]

data_sorted = sorted(data.items(), key=operator.itemgetter(1))
with open("nidurstodur/oftar_en_fimm.txt","w") as f:
    for i in reversed(range(0,len(data_sorted))):

        f.write("{}\t{}\t{}\n".format(data_sorted[i][0], data_sorted[i][1], data_eldra[data_sorted[i][0]]))

#list yfir orð sem birtust helmingi oftar í ár en árið á undan
data = {}
for lemma in data_lastyear:

    if data_lastyear[lemma]>=10:
        if lemma in data_curryear:
            if data_curryear[lemma] < data_lastyear[lemma]/4:
                data[lemma] = data_lastyear[lemma]

data_sorted = sorted(data.items(), key=operator.itemgetter(1))
with open("nidurstodur/faekkun.txt","w") as f:
    for i in reversed(range(0,len(data_sorted))):

        f.write("{}\t{}\t{}\n".format(data_sorted[i][0], data_sorted[i][1], data_curryear[data_sorted[i][0]]))
