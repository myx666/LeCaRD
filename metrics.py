# -*- encoding: utf-8 -*-
'''
@Func    :   evaluation of retrieved results
@Time    :   2021/03/04 17:35:21
@Author  :   Yixiao Ma 
@Contact :   mayx20@mails.tsinghua.edu.cn
'''

import os
import numpy as np
import json
import math
import functools
import argparse
# from sklearn.metrics import ndcg_score
from tqdm import tqdm

def kappa(testData, k): #testData表示要计算的数据，k表示数据矩阵的是k*k的
    dataMat = np.mat(testData)
    P0 = 0.0
    for i in range(k):
        P0 += dataMat[i, i]*1.0
    xsum = np.sum(dataMat, axis=1)
    ysum = np.sum(dataMat, axis=0)
    #xsum是个k行1列的向量，ysum是个1行k列的向量
    Pe  = float(ysum*xsum)/k**2
    P0 = float(P0/k*1.0)
    cohens_coefficient = float((P0-Pe)/(1-Pe))
    return cohens_coefficient

def fleiss_kappa(testData, N, k, n): 
    dataMat = np.mat(testData, float)
    oneMat = np.ones((k, 1))
    sum = 0.0
    P0 = 0.0
    for i in range(N):
        temp = 0.0
        for j in range(k):
            sum += dataMat[i, j]
            temp += 1.0*dataMat[i, j]**2
        temp -= n
        temp /= (n-1)*n
        P0 += temp
    P0 = 1.0*P0/N
    ysum = np.sum(dataMat, axis=0)
    for i in range(k):
        ysum[0, i] = (ysum[0, i]/sum)**2 # (1/k)**2
    Pe = ysum*oneMat*1.0
    ans = (P0-Pe)/(1-Pe)
    return ans[0, 0]

# def ndcg(ranks,K):
#     dcg_value = 0.
#     idcg_value = 0.
#     log_ki = []

#     sranks = sorted(ranks, reverse=True)

#     for i in range(0,K):
#         logi = math.log(i+2,2)
#         dcg_value += ranks[i] / logi
#         idcg_value += sranks[i] / logi

#     return dcg_value/idcg_value

def ndcg(ranks, gt_ranks, K):
    dcg_value = 0.
    idcg_value = 0.
    # log_ki = []

    sranks = sorted(gt_ranks, reverse=True)

    for i in range(0,K):
        logi = math.log(i+2,2)
        dcg_value += ranks[i] / logi
        idcg_value += sranks[i] / logi

    return dcg_value/idcg_value

def load_file(args):

    label_dic = json.load(open(args.label, 'r'))
    # with open(os.path.join(args.pred, 'bert.json'), 'r') as f:
    #     blines = f.readlines()
    # bertdics = [eval(blines[0]),eval(blines[1]),eval(blines[2]),eval(blines[3])]
    tdic = json.load(open(os.path.join(args.pred, 'tfidf_top100.json'), 'r'))
    ldic = json.load(open(os.path.join(args.pred, 'lm_top100.json'), 'r'))
    bdic = json.load(open(os.path.join(args.pred, 'bm25_top100.json'), 'r'))

    for key in list(label_dic.keys())[:]:
        tdic[key].reverse()
        bdic[key].reverse()

    # with open('/work/mayixiao/lawformer/lawformer_top30.json', 'r') as f:
    #     lawformer_dic = json.load(f)
    
    return label_dic, [tdic, bdic, ldic]#, lawformer_dic

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Help info:")
    parser.add_argument('--m', type=str, choices= ['NDCG', 'P', 'MAP', 'KAPPA'], default='NDCG', help='Metric.')
    parser.add_argument('--label', type=str, default='data/label/label_top30_dict.json', help='Label file path.')
    parser.add_argument('--pred', type=str, default='data/prediction', help='Prediction dir path.')
    parser.add_argument('--q', type=str, choices= ['all', 'common', 'controversial', 'test', 'test_2'], default='all', help='query set')

    args = parser.parse_args()
    
    label_dic, dics = load_file(args)
    
    if args.q == 'all':
        keys = list(label_dic.keys())
    elif args.q == 'common':
        keys = list(label_dic.keys())[:77]  
    elif args.q == 'controversial':
        keys = list(label_dic.keys())[77:]
    elif args.q == 'test':
        # combdic = json.load(open('/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/prediction/combined_top100.json','r'))
        keys = [i for i in list(label_dic.keys()) if list(label_dic.keys()).index(i) % 5 == 0]
        # keys = [i for i in list(combdic.keys()) if list(combdic.keys()).index(i) % 5 == 0]
        # keys = label_dic.keys()
    elif args.q == 'test_2':
        keys = label_dic.keys()
    
    if args.m == 'NDCG':
        topK_list = [10, 20, 30]
        ndcg_list = []
        for topK in topK_list:
            temK_list = []
            for dic in dics:
                sndcg = 0.0
                for key in keys:
                    rawranks = []
                    for i in dic[key]:
                        if str(i) in list(label_dic[key])[:30]:
                            rawranks.append(label_dic[key][str(i)])
                        else:
                            rawranks.append(0)
                    ranks = rawranks + [0]*(30-len(rawranks))
                    if sum(ranks) != 0:
                        sndcg += ndcg(ranks, list(label_dic[key].values()), topK)
                temK_list.append(sndcg/len(keys))
            ndcg_list.append(temK_list)
        print(ndcg_list)

    elif args.m == 'P': 
        topK_list = [5,10]
        sp_list = []

        for topK in topK_list:
            temK_list = []
            for dic in dics:
                sp = 0.0
                for key in keys:
                    ranks = [i for i in dic[key] if str(i) in list(label_dic[key][:30])] 
                    sp += float(len([j for j in ranks[:topK] if label_dic[key][str(j)] == 3])/topK)
                temK_list.append(sp/len(keys))
            sp_list.append(temK_list)
        print(sp_list)

    elif args.m == 'MAP':
        map_list = []
        for dic in dics:
            smap = 0.0
            for key in keys:
                ranks = [i for i in dic[key] if str(i) in list(label_dic[key][:30])] 
                rels = [ranks.index(i) for i in ranks if label_dic[key][str(i)] == 3]
                tem_map = 0.0
                for rel_rank in rels:
                    tem_map += float(len([j for j in ranks[:rel_rank+1] if label_dic[key][str(j)] == 3])/(rel_rank+1))
                if len(rels) > 0:
                    smap += tem_map / len(rels)
            map_list.append(smap/len(keys))
        print(map_list)
    
    elif args.m == 'KAPPA':
        lists = json.load(open('/work/mayixiao/similar_case/LeCaRD/private/data/label_top30.json', 'r'))
        dataArr = []

        for i in lists[0].keys():
            for j in range(30):
                tem = [0,0,0,0]
                for k in range(3):
                    tem[int(lists[k][i][j])-1] += 1
                dataArr.append(tem)
        print(fleiss_kappa(dataArr, 30*len(lists[0]), 4, 3))

    # elif MODE == 'F1':
    #     topK = 15
    #     rdic_list = [tdic, ldic, bdic]
    #     f1_list = []
    #     for rdic in rdic_list:
    #         k = 0
    #         sf1 = 0.0
    #         for key in list(combdic.keys())[:100]:
    #             pre = 0.0
    #             recall = 0.0
    #             ranks = [i for i in rdic[key] if i in list(combdic[key][:30])] 
    #             pre = float(len([j for j in ranks[:topK] if label_dic[k][list(combdic[key][:30]).index(j)] == 1])/topK)
    #             allrel = len([j for j in ranks[:] if label_dic[k][list(combdic[key][:30]).index(j)] == 1])
    #             if allrel > 0 and pre > 0:
    #                 recall = float(len([j for j in ranks[:topK] if label_dic[k][list(combdic[key][:30]).index(j)] == 1])/allrel)
    #                 sf1 += 2/(1/pre+1/recall)
    #             k += 1
    #         f1_list.append(sf1/100)

    #     print(f1_list)
    

