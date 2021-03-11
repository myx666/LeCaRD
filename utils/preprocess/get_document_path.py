# -*- encoding: utf-8 -*-
'''
@Func    :   get criminal document paths from raw corpus
@Time    :   2021/03/05 15:00:39
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
parser.add_argument('--w', type=str, default='data/corpus/document_path2.json', help='Write path.')

args = parser.parse_args()

iscriminal = re.compile(r'.*罪.*')
isverdict = re.compile(r'.*刑事判决书.*')
raw_dirs = os.listdir(args.d)
dirs = [dir_ for dir_ in raw_dirs if os.path.isdir(os.path.join(args.d, dir_))]
jspaths = {'single':[],'retrial':[]} #刑事案件判决书的路径、有再审判决书的路径

for dir in tqdm(dirs[:]):
    dirpath = os.path.join(args.d, dir)
    if os.path.isdir(dirpath):
        files = [_file for _file in os.listdir(dirpath) if os.path.isdir(dirpath) and os.path.isfile(os.path.join(dirpath, _file))]
    tem_retrival = []
    # with open(os.path.join(dirpath,files[0]), 'r') as f: # 检验相同案件下文书名称是否相同
    #     jsfile = json.load(f)
    #     if 'ajName' in jsfile:
    #         name = jsfile['ajName']
    #     else:
    #         print('no ajName: ', os.path.join(dirpath,files[0]))
    for file_ in files:
        with open(os.path.join(dirpath,file_), 'r') as f:
            jsfile = json.load(f)
        
        if 'ajjbqk' in jsfile:
            if 'writName' in jsfile:
                if isverdict.match(jsfile['writName']):
                    tem_retrival.append(os.path.join(dir,file_))
            # elif 'ajName' in jsfile and iscriminal.match(jsfile['ajName']):
                # print('no writName: ', os.path.join(args.d, dir, file_))

    if len(tem_retrival) == 1:
        jspaths['single'].append(tem_retrival[0])
    elif len(tem_retrival) > 1:
        jspaths['retrial'].append(tem_retrival)

with open(args.w, 'w') as g:
    json.dump(jspaths, g, ensure_ascii=False)

print(len(jspaths['single']), len(jspaths['retrial']))
