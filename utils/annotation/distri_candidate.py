# -*- encoding: utf-8 -*-
'''
@Func    :   distribute candidates for annotation
@Time    :   2021/03/05 12:12:03
@Author  :   Yixiao Ma 
@Contact :   mayx20@mails.tsinghua.edu.cn
'''

import os
import re
import numpy as np
import json
import argparse
from shutil import copy
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Help info.")
parser.add_argument('--d', type=str, default='data/corpus/documents', help='Document dir path.')
parser.add_argument('--q', type=str, default='data/prediction/combined_top100.json', help='Query path.') # query.json
parser.add_argument('--w', type=str, default='/work/mayixiao/similar_case/candidates1', help='Write path.')

args = parser.parse_args()

# with open(args.q, 'r') as g:
#     qs = g.readlines()

# for i in range(107):
#     temc = eval(qs[i])['candidate']
#     # print(len(temc))
#     j = 1
#     for cand in temc:
#         temqw = ''
#         with open(os.path.join(args.c, cand), 'r') as f:
#             temqw = json.load(f)['qw'].replace(' ', '\n')
#         with open(os.path.join(args.w, str(i+1),str(i+1)+'-'+str(j)+'.txt'),'w') as f:
#             f.write(temqw)
#         j += 1
#     # with open(os.path.join(WROOT,str(i+1),'q.txt'),'w') as f:
#     #     f.write(temq)

root = '/work/yangjun/LAW/preprocess_new_data/feature_data'
with open('data/corpus/document_path.json', 'r') as f:
    jsfile = json.load(f)

paths = []
for i in jsfile['single']:
    paths.append(i)

for j in jsfile['retrial']:
    for i in j:
        paths.append(i)

print(len(paths))

# print('/work/yangjun/LAW/preprocess_new_data/feature_data/'+paths[36655])

with open(args.q, 'r') as f:
    qs = json.load(f)

for key in tqdm(list(qs.keys())[:50]):
    keydir = os.path.join(args.w, key)
    if not os.path.exists(keydir):
        os.mkdir(keydir)
        for cand_num in qs[key]:
            cpath = os.path.join(root, paths[cand_num]) 
            copy(cpath, os.path.join(keydir, str(cand_num)+'.json'))



            
