# -*- encoding: utf-8 -*-
'''
@Func    :   get candidate pools by tf-idf
@Time    :   2021/03/05 17:13:42
@Author  :   Yixiao Ma 
@Contact :   mayx20@mails.tsinghua.edu.cn
'''

import jieba
import os
import re
import numpy as np
import json
import argparse
from tqdm import tqdm
from gensim import corpora,models,similarities

parser = argparse.ArgumentParser(description="Help info.")
parser.add_argument('--s', type=str, default='data/others/stopword.txt', help='Stopword path.')
parser.add_argument('--q', type=str, default='data/query/query.json', help='Query path.')
parser.add_argument('--split', type=str, default='data/others/corpus_jieba.json', help='Split corpus path.')
parser.add_argument('--w', type=str, default='data/prediction/tfidf_top100.json', help='Write path.')

args = parser.parse_args()

with open(args.q, 'r') as f:
    lines = f.readlines()

with open(args.split, 'r') as f:
    raw_corpus = json.load(f)

with open(args.s, 'r') as g:
    words = g.readlines()
stopwords = [i.strip() for i in words]
stopwords.extend(['.','（','）','-'])

#创建词典
dictionary = corpora.Dictionary(raw_corpus)
#获取语料库
corpus = [dictionary.doc2bow(i) for i in raw_corpus]
tfidf = models.TfidfModel(corpus)
#特征数
featureNUM = len(dictionary.token2id.keys())
#通过TfIdf对整个语料库进行转换并将其编入索引，以准备相似性查询
index = similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=featureNUM)
#稀疏向量.dictionary.doc2bow(doc)是把文档doc变成一个稀疏向量，[(0, 1), (1, 1)]，表明id为0,1的词汇出现了1次，至于其他词汇，没有出现。

rankdic = {}
for line in tqdm(lines[:]):
    a = jieba.cut(eval(line)['q'], cut_all=False)
    tem = " ".join(a).split()
    q = [i for i in tem if not i in stopwords]
    new_vec = dictionary.doc2bow(q)
    #计算向量相似度
    sim = index[tfidf[new_vec]]
    rankdic[eval(line)['ridx']] = np.array(sim).argsort()[-101:].tolist()
    # print(sim[:5])
    # print(np.array(bm25Model.get_scores(q)).argsort()[-5:].tolist())
with open(args.w, 'w') as f:
    json.dump(rankdic, f, ensure_ascii=False)