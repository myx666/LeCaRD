# -*- encoding: utf-8 -*-
'''
@Func    :   get word-level corpus
@Time    :   2021/03/05 16:47:38
@Author  :   Yixiao Ma 
@Contact :   mayx20@mails.tsinghua.edu.cn
'''

import os
import re
import numpy as np
import json
import argparse
from tqdm import tqdm
# import thulac
import jieba
from sys import path
path.append("/work/mayixiao/www22")
from pre_ajjbqk import process_ajjbqk

parser = argparse.ArgumentParser(description="Help info.")
parser.add_argument('--d', type=str, default='/work/yangjun/LAW/preprocess_new_data/feature_data', help='Document dir path.')
parser.add_argument('--dpath', type=str, default='/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/corpus/document_path.json', help='Document_path file path.')
parser.add_argument('--s', type=str, default='/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/others/stopword.txt', help='Stopword path.')
parser.add_argument('--w', type=str, default='/work/mayixiao/similar_case/202006/corpus_jieba_short.json', help='Write path.')

args = parser.parse_args()

# seg = thulac.thulac(seg_only=True, filt=True)

with open(args.dpath, 'r') as f:
    jspath = json.load(f)

with open(args.s, 'r') as g:
    lines = g.readlines()
stopwords = [i.strip() for i in lines]
stopwords.extend(['.','（','）','-'])

corpus = []

for path in tqdm(jspath['single'][:]):
    fullpath = os.path.join(args.d, path)
    with open(fullpath, 'r') as g:
        file_ = json.load(g)
    # if 'ajjbqk' in file_:
    processed_file = process_ajjbqk(file_['ajjbqk'])
    a = jieba.cut(processed_file, cut_all=False)
    # a = jieba.cut(file_['ajjbqk'], cut_all=False)
    tem = " ".join(a).split()
    # tem = seg.cut(file_['ajjbqk'], text = True).split()
    corpus.append([i for i in tem if not i in stopwords])

for path0 in tqdm(jspath['retrial'][:]):
    for path in path0:
        fullpath = os.path.join(args.d, path)
        with open(fullpath, 'r') as g:
            file_ = json.load(g)
        # if 'ajjbqk' in file_:
        a = jieba.cut(file_['ajjbqk'], cut_all=False)
        tem = " ".join(a).split()
        # tem = seg.cut(file_['ajjbqk'], text = True).split()
        corpus.append([i for i in tem if not i in stopwords])

print(len(corpus))
with open(args.w, 'w') as f:
    json.dump(corpus, f, ensure_ascii=False)

