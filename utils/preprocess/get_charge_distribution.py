# -*- encoding: utf-8 -*-
'''
@Func    :   get charge distribution of common documents or controversial documents
@Time    :   2021/03/05 14:38:17
@Author  :   Yixiao Ma 
@Contact :   mayx20@mails.tsinghua.edu.cn
'''

import re
import tqdm
import os
import json
import argparse

parser = argparse.ArgumentParser(description="Help info.")
parser.add_argument('--c', type=str, default='data/corpus', help='Corpus dir path.')
parser.add_argument('--clist', type=str, default='data/others/criminal charges.txt', help='Charge list.')
parser.add_argument('--w', type=str, choices= ['common', 'controversial'], default='common', help='Type of charge paths.')

args = parser.parse_args()

charges = []
ans = {}
with open(os.path.join(args.c, 'document_path.json'), 'r') as f:
    jspath = json.load(f)

with open(args.clist, 'r') as k:
    lines = k.readlines()

res = [re.compile(line[:-2]) for line in lines]
count = 0
# count2 = 0
if args.w == 'common':
    _type = 'single'
    LABELPATH = os.path.join(args.c, 'common_charge.json')
else:
    _type = 'retrial'
    LABELPATH = os.path.join(args.c, 'controversial_charge.json')

for path in jspath[_type][:]:
    # for path in paths:
    fullpath = os.path.join(args.c, 'documents', path)
    with open(fullpath, 'r') as g:
        file_ = json.load(g)
    flag = 0
    for crime in res:
        if crime.search(file_['writName']):
            charge = crime.search(file_['writName']).group()+'罪'
            # count2 += 1
            if charge in ans:
                ans[charge].append(path)
            else:
                ans[charge] = [path]
            flag = 1
    if flag == 0:
        print(fullpath)
        count += 1

print(count)
print(sum([len(ans[i]) for i in ans.keys()]))
# with open(LABELPATH, 'a') as h:
#     json.dump(ans, h, ensure_ascii=False)

print(len(ans.keys()))

