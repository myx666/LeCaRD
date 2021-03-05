# -*- encoding: utf-8 -*-
'''
@Func    :   get query file: common query + controversial query
@Time    :   2021/03/05 11:17:20
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
parser.add_argument('--q', type=str, default='data/query', help='Query dir path.')
parser.add_argument('--w', type=str, default='data/query/query.json', help='Write path.')

args = parser.parse_args()

jswrite = []

with open(os.path.join(args.q, 'common_query.json'), 'r') as f:
    lines = f.readlines()

with open(os.path.join(args.q, 'controversial_query.json'), 'r') as f:
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

with open(args.w, 'w') as f:
    for line in jswrite:
        json.dump(line,f, ensure_ascii=False)
        f.write('\n')


