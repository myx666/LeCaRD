# 构造训练bert的文件

import os
import re
import numpy as np
import json
from tqdm import tqdm

ROOT = '/work/yangjun/LAW/preprocess_new_data/feature_data'
CRIME_ROOT = '/work/mayixiao/similar_case/crimepath.json'
Q_PATH = '/work/mayixiao/similar_case/tolabel.json'
WRITE_ROOT = '/work/mayixiao/similar_case/BERT/'
L_PATH = '/work/mayixiao/similar_case/LeCaRD/label/label.json'

jstrain = []
jstest = []

with open(Q_PATH, 'r') as f:
    lines = f.readlines()

with open(L_PATH, 'r') as f:
    labels = json.load(f)[3]

for i in tqdm(range(100)):
    dic = eval(lines[i])
    for j in range(30):
        tem = {}
        tem['guid'] = str(dic['ridx']) + '_' + str(j)
        tem['text_a'] = dic['q']
        with open(os.path.join(ROOT,dic['candidate'][j]), 'r') as f:
            tem['text_b'] = json.load(f)['ajjbqk']
        if labels[i][j] == 1:
            tem['label'] = 1 
        else:
            tem['label'] = 0
        if i % 5 != 0:
            jstrain.append(tem)
        else:
            jstest.append(tem)

with open(WRITE_ROOT+'train.json', 'w') as f:
    for line in jstrain:
        json.dump(line,f, ensure_ascii=False)
        f.write('\n')

with open(WRITE_ROOT+'test.json', 'w') as f:
    for line in jstest:
        json.dump(line,f, ensure_ascii=False)
        f.write('\n')