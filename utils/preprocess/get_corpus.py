import os
import re
import numpy as np
import json
from tqdm import tqdm
# import thulac
import jieba

ROOT = '/work/yangjun/LAW/preprocess_new_data/feature_data'
CRIME_ROOT = '/work/mayixiao/similar_case/crimepath.json'
Q_PATH = '/work/mayixiao/similar_case/普通query+fx.json'
STOP_PATH = '/work/mayixiao/similar_case/stopword.txt'
WRITEPATH = '/work/mayixiao/similar_case/corpus_jieba.json'

# seg = thulac.thulac(seg_only=True, filt=True)

with open(CRIME_ROOT, 'r') as f:
    jspath = json.load(f)

with open(STOP_PATH, 'r') as g:
    lines = g.readlines()
stopwords = [i.strip() for i in lines]
stopwords.extend(['.','（','）','-'])

corpus = []

for path in tqdm(jspath['single'][:]):
    fullpath = os.path.join(ROOT, path)
    with open(fullpath, 'r') as g:
        file_ = json.load(g)
    # if 'ajjbqk' in file_:
    a = jieba.cut(file_['ajjbqk'], cut_all=False)
    tem = " ".join(a).split()
    # tem = seg.cut(file_['ajjbqk'], text = True).split()
    corpus.append([i for i in tem if not i in stopwords])

for path0 in tqdm(jspath['retrial'][:]):
    for path in path0:
        fullpath = os.path.join(ROOT, path)
        with open(fullpath, 'r') as g:
            file_ = json.load(g)
        # if 'ajjbqk' in file_:
        a = jieba.cut(file_['ajjbqk'], cut_all=False)
        tem = " ".join(a).split()
        # tem = seg.cut(file_['ajjbqk'], text = True).split()
        corpus.append([i for i in tem if not i in stopwords])

print(len(corpus))
with open(WRITEPATH, 'w') as f:
    json.dump(corpus, f, ensure_ascii=False)

