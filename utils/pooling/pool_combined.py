import os
import re
import numpy as np
import json
from tqdm import tqdm
import lmir
import random

ROOT = '/work/yangjun/LAW/preprocess_new_data/feature_data'
CRIME_ROOT = '/work/mayixiao/similar_case/crimepath.json'
Q_PATH = '/work/mayixiao/similar_case/tolabel.json'
STOP_PATH = '/work/mayixiao/similar_case/stopword.txt'
CORPUS_PATH = '/work/mayixiao/similar_case/corpus_jieba.json'
TFIDF_PATH = '/work/mayixiao/similar_case/tfidf_top100.json'
BM25_PATH = '/work/mayixiao/similar_case/bm25_top100.json'
LM_PATH = '/work/mayixiao/similar_case/lm_top100.json'
DISTRI_PATH = '/work/mayixiao/similar_case/chargelabel.json'
WRITE_PATH = '/work/mayixiao/similar_case/combined_top100.json'

# with open(CORPUS_PATH,'r') as f:
#     corpus = json.load(f)

# print(len(corpus))
# with open(CRIME_ROOT,'r') as f:
#     jspath = json.load(f)

with open(LM_PATH,'r') as f:
    lm_dic = json.load(f)

with open(BM25_PATH,'r') as f:
    bm_dic = json.load(f)

with open(TFIDF_PATH,'r') as f:
    tf_dic = json.load(f)

a = lm_dic
b = bm_dic
c = tf_dic

# pall = 0
wdic = {}

for key in a.keys():
    leng = len(a[key])
    tem = []
    for i in a[key][1:]:
        if i in b[key][:-1] and i in c[key][:-1]:
            tem.append(i)
    for i in a[key][1:]:
        if i in b[key][:-1] and i not in tem:
            tem.append(i)
    d = c[key].copy()
    d.reverse()
    for i in d[1:]:
        if (i in a[key][1:] or i in b[key][:-1]) and i not in tem:
            tem.append(i)
    tem = tem[:67]
    while len(tem) < 100:
        new = random.randint(0,43823)
        while new in tem:
            new = random.randint(0,43823)
        tem.append(new)
    wdic[key] = tem
    # print(len(tem))

with open(WRITE_PATH,'w') as g:
    json.dump(wdic, g, ensure_ascii=False)

# ---------------------------------

with open(CRIME_ROOT, 'r') as f:
    jspath = json.load(f)

paths = []

for path in tqdm(jspath['single'][:]):
    paths.append(path)

for path0 in tqdm(jspath['retrial'][:]):
    for path in path0:
        paths.append(path)

top30 = {}
for key in a.keys():
    top30[key] = [paths[i] for i in wdic[key][:30]]
    print(wdic[key][:30])
    print(top30[key])

with open('/work/mayixiao/similar_case/tolabel2.json', 'r') as f:
    lines = f.readlines()

ans = []
for line in lines:
    tem = eval(line)
    tem['candidate'] = top30[str(tem['ridx'])]
    ans.append(tem)

# with open('/work/mayixiao/similar_case/tolabel.json', 'w') as f:
#     for line in ans:
#         json.dump(line,f, ensure_ascii=False)
#         f.write('\n')