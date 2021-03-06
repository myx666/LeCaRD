# -*- encoding: utf-8 -*-
'''
@Func    :   get candidate pools by combined methods
@Time    :   2021/03/05 17:16:40
@Author  :   Yixiao Ma 
@Contact :   mayx20@mails.tsinghua.edu.cn
'''

import os
import re
import numpy as np
import json
import argparse
from tqdm import tqdm
import lmir
import random

parser = argparse.ArgumentParser(description="Help info.")
parser.add_argument('--d', type=str, default='data/corpus/documents', help='Document dir path.')
parser.add_argument('--t', type=str, default='data/prediction/tfidf_top100.json', help='TF-IDF prediction path.')
parser.add_argument('--b', type=str, default='data/prediction/bm25_top100.json', help='BM25 prediction path.')
parser.add_argument('--l', type=str, default='data/prediction/lm_top100.json', help='Language Models prediction path.')
parser.add_argument('--w', type=str, default='data/prediction/combined_top100.json', help='Write path.')

args = parser.parse_args()

with open(args.l, 'r') as f:
    lm_dic = json.load(f)

with open(args.b, 'r') as f:
    bm_dic = json.load(f)

with open(args.t, 'r') as f:
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
    # tem = tem[:67]
    tem = tem[:30]
    while len(tem) < 100:
        new = random.randint(0,43823)
        while new in tem:
            new = random.randint(0,43823)
        tem.append(new)
    wdic[key] = tem
    # print(len(tem))

with open(args.w, 'w') as g:
    json.dump(wdic, g, ensure_ascii=False)

# ---------------------------------

# with open(args.d, 'r') as f:
#     jspath = json.load(f)

# paths = []

# for path in tqdm(jspath['single'][:]):
#     paths.append(path)

# for path0 in tqdm(jspath['retrial'][:]):
#     for path in path0:
#         paths.append(path)

# top30 = {}
# for key in a.keys():
#     top30[key] = [paths[i] for i in wdic[key][:30]]
#     print(wdic[key][:30])
#     print(top30[key])

# with open('/work/mayixiao/similar_case/tolabel2.json', 'r') as f:
#     lines = f.readlines()

# ans = []
# for line in lines:
#     tem = eval(line)
#     tem['candidate'] = top30[str(tem['ridx'])]
#     ans.append(tem)

# with open('/work/mayixiao/similar_case/tolabel.json', 'w') as f:
#     for line in ans:
#         json.dump(line,f, ensure_ascii=False)
#         f.write('\n')