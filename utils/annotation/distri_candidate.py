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
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Help info.")
parser.add_argument('--d', type=str, default='data/corpus/documents', help='Document dir path.')
parser.add_argument('--q', type=str, default='data/query/query.json', help='Query path.')
parser.add_argument('--w', type=str, default='/work/mayixiao/similar_case/类案数据集标注', help='Write path.')

args = parser.parse_args()

with open(args.q, 'r') as g:
    qs = g.readlines()

for i in range(107):
    temc = eval(qs[i])['candidate']
    # print(len(temc))
    j = 1
    for cand in temc:
        temqw = ''
        with open(os.path.join(args.c, cand), 'r') as f:
            temqw = json.load(f)['qw'].replace(' ', '\n')
        with open(os.path.join(args.w, str(i+1),str(i+1)+'-'+str(j)+'.txt'),'w') as f:
            f.write(temqw)
        j += 1
    # with open(os.path.join(WROOT,str(i+1),'q.txt'),'w') as f:
    #     f.write(temq)
