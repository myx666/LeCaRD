# -*- encoding: utf-8 -*-
'''
@Func    :   transfer file to bert-readable style
@Time    :   2021/03/04 17:36:47
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
parser.add_argument('--l', type=str, default='data/label/label.json', help='Label file path.')
parser.add_argument('--q', type=str, default='data/query/query.json', help='Query file path.')
parser.add_argument('--d', type=str, default='data/corpus/documents', help='Document dir path.')
parser.add_argument('--w', type=str, default='.', help='Write file path.')

args = parser.parse_args()

jstrain = []
jstest = []
with open(args.q, 'r') as f:
    lines = f.readlines()

with open(args.l, 'r') as f:
    labels = json.load(f)[3]

for i in tqdm(range(100)):
    dic = eval(lines[i])
    for j in range(30):
        tem = {}
        tem['guid'] = str(dic['ridx']) + '_' + str(j)
        tem['text_a'] = dic['q']
        with open(os.path.join(args.d, dic['candidate'][j]), 'r') as f:
            tem['text_b'] = json.load(f)['ajjbqk']
        if labels[i][j] == 1:
            tem['label'] = 1 
        else:
            tem['label'] = 0
        if i % 5 != 0:
            jstrain.append(tem)
        else:
            jstest.append(tem)

with open(args.w + 'train.json', 'w') as f:
    for line in jstrain:
        json.dump(line,f, ensure_ascii=False)
        f.write('\n')

with open(args.w + 'test.json', 'w') as f:
    for line in jstest:
        json.dump(line,f, ensure_ascii=False)
        f.write('\n')