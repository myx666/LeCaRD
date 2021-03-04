import os
import re
import numpy as np
import json
from tqdm import tqdm
# import thulac
import jieba

ROOT = '/work/yangjun/LAW/preprocess_new_data/feature_data'
CRIME_ROOT = '/work/mayixiao/similar_case/crimepath.json'
Q_PATH = '/work/mayixiao/similar_case/普通query+fx.json'
W_PATH = '/work/mayixiao/similar_case/tolabel.json'
C_PATH = '/work/mayixiao/similar_case/combined_top100.json'

# with open(CRIME_ROOT, 'r') as f:
#     jspath = json.load(f)

# paths = []

# for path in tqdm(jspath['single'][:]):
#     paths.append(path)

# for path0 in tqdm(jspath['retrial'][:]):
#     for path in path0:
#         paths.append(path)

jswrite = []

with open(Q_PATH, 'r') as f:
    lines = f.readlines()



with open('/work/mayixiao/similar_case/改判query.json', 'r') as f:
    jsfile = json.load(f)

for line in lines:
    dic = eval(line)
    tem = {}
    tem['path'] = dic['path']
    tem['ridx'] = dic['ridx']
    tem['q'] = dic['jbqk']
    tem['crime'] = dic['crime']
    jswrite.append(tem)


lists = jsfile.values()
count = 0
for list_ in lists:
    for case in list_:
        tem = {}
        tem['path'] = case['id']
        tem['ridx'] = count
        tem['q'] = case['q']
        tem['crime'] = [case['target']]
        jswrite.append(tem)
        count += 1

print(len(jswrite))

with open(W_PATH, 'w') as f:
    for line in jswrite:
        json.dump(line,f, ensure_ascii=False)
        f.write('\n')


