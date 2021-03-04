import os
import re
import numpy as np
import json
from tqdm import tqdm
from gensim.summarization import bm25
import jieba

ROOT = '/work/yangjun/LAW/preprocess_new_data/feature_data'
CRIME_ROOT = '/work/mayixiao/similar_case/crimepath.json'
Q_PATH = '/work/mayixiao/similar_case/tolabel.json'
STOP_PATH = '/work/mayixiao/similar_case/stopword.txt'
CORPUS_PATH = '/work/mayixiao/similar_case/corpus_jieba.json'
WRITE_PATH = '/work/mayixiao/similar_case/bm25_top100.json'

with open(CORPUS_PATH,'r') as f:
    corpus = json.load(f)

with open(STOP_PATH, 'r') as g:
    words = g.readlines()
stopwords = [i.strip() for i in words]
stopwords.extend(['.','（','）','-'])

with open(Q_PATH,'r') as f:
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

with open(WRITE_PATH, 'w') as f:
    json.dump(rankdic, f, ensure_ascii=False)
    