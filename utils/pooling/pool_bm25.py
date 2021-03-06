# -*- encoding: utf-8 -*-
'''
@Func    :   get candidate pools by bm25
@Time    :   2021/03/05 17:01:03
@Author  :   Yixiao Ma 
@Contact :   mayx20@mails.tsinghua.edu.cn
'''

import os
import re
import numpy as np
import json
from tqdm import tqdm
import argparse
from gensim.summarization import bm25
import jieba

parser = argparse.ArgumentParser(description="Help info.")
parser.add_argument('--s', type=str, default='data/others/stopword.txt', help='Stopword path.')
parser.add_argument('--q', type=str, default='data/query/query.json', help='Query path.')
parser.add_argument('--split', type=str, default='data/others/corpus_jieba.json', help='Split corpus path.')
parser.add_argument('--w', type=str, default='data/prediction/bm25_top100.json', help='Write path.')

args = parser.parse_args()

with open(args.split, 'r') as f:
    corpus = json.load(f)

with open(args.s, 'r') as g:
    words = g.readlines()
stopwords = [i.strip() for i in words]
stopwords.extend(['.','（','）','-'])

with open(args.q, 'r') as f:
    lines = f.readlines()

bm25Model = bm25.BM25(corpus)
print(len(corpus))
rankdic = {}
for line in tqdm(lines[:]):
    a = jieba.cut(eval(line)['q'], cut_all=False)
    tem = " ".join(a).split()
    q = [i for i in tem if not i in stopwords]
    rankdic[eval(line)['ridx']] = np.array(bm25Model.get_scores(q)).argsort()[-101:].tolist()
    # print(eval(line)['ridx'], corpus[np.array(bm25Model.get_scores(q)).argsort()[-2]])

with open(args.w, 'w') as f:
    json.dump(rankdic, f, ensure_ascii=False)
    