import os
import numpy as np
import json
import math
import functools
from sklearn.metrics import ndcg_score
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

def fleiss_kappa(testData, N, k, n): #testData表示要计算的数据，（N,k）表示矩阵的形状，说明数据是N行j列的，一共有n个标注人员
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
        ysum[0, i] = (1/k)**2#(ysum[0, i]/sum)**2
    Pe = ysum*oneMat*0.0
    ans = (P0-Pe)/(1-Pe)
    return ans[0, 0]

def ndcg(ranks,K):
    dcg_value = 0.
    idcg_value = 0.
    log_ki = []

    sranks = sorted(ranks, reverse=True)

    for i in range(0,K):
        logi = math.log(i+2,2)
        dcg_value += ranks[i] / logi
        idcg_value += sranks[i] / logi

    '''print log_ki'''
    # print ("DCG value is " + str(dcg_value))
    # print ("iDCG value is " + str(idcg_value))

    return dcg_value/idcg_value

if __name__ == "__main__":
    with open('/work/mayixiao/similar_case/LeCaRD/label/label.json', 'r') as f:
        lists = json.load(f)
    avglist = lists[3]
    with open('/work/mayixiao/similar_case/LeCaRD/label/bert.json', 'r') as f:
        blines = f.readlines()
    bertdics = [eval(blines[0]),eval(blines[1]),eval(blines[2]),eval(blines[3])]
    with open('/work/mayixiao/similar_case/combined_top100.json','r') as f:
        combdic = json.load(f)
    with open('/work/mayixiao/similar_case/tfidf_top100.json','r') as f:
        tdic = json.load(f)
    with open('/work/mayixiao/similar_case/lm_top100.json','r') as f:
        ldic = json.load(f)
    with open('/work/mayixiao/similar_case/bm25_top100.json','r') as f:
        bdic = json.load(f)

    for key in list(combdic.keys())[:100]:
        tdic[key].reverse()
        bdic[key].reverse()
    MODE = 'MAP'
    keys = list(combdic.keys())[:77]
    # keys = [i for i in list(combdic.keys())[:100] if list(combdic.keys())[:100].index(i) % 5 == 0]
    dics = [bdic, tdic, ldic]
    # dics = [eval(blines[0]),eval(blines[1]),eval(blines[2]),eval(blines[3])]
    
    if MODE == 'KAPPA':
        dataArr = []
        for i in range(100):
            rel = 0
            for j in range(30):
                # temcount = [0,0,0,0] # number of label 1,2,3,4
                tem = 0
                for k in range(3):
                    # temcount[int(lists[k][i][j])-1] += 1
                    tem += lists[k][i][j]
                if tem <= 4:
                    rel += 1
                # dataArr.append(temcount)
            dataArr.append(rel)
        # print(dataArr)
        # print(sum(dataArr)/len(dataArr))
        print(len([i for i in dataArr if i==0 and i < 5]))
        # print(fleiss_kappa(dataArr, 3000, 4, 3))
    elif MODE == 'NDCG':
        topK_list = [10, 20, 30]

        ndcg_list = []
        for topK in topK_list:
            temK_list = []
            for redic in dics:
                sndcg = 0.0
                for key in keys:
                    rawranks = [4 - avglist[list(combdic.keys()).index(key)][list(combdic[key][:30]).index(i)] for i in redic[key] if i in list(combdic[key][:30])]
                    # print(rawranks) 
                    ranks = rawranks + [0]*(30-len(rawranks))
                    if sum(ranks) != 0:
                        sndcg += ndcg(ranks,topK)
                temK_list.append(sndcg/len(keys))
            ndcg_list.append(temK_list)
        print(ndcg_list)

    elif MODE == 'P': # P and MAP
        topK_list = [5,10]
        sp_list = []

        for topK in topK_list:
            temK_list = []
            for rdic in dics:
                sp = 0.0
                for key in keys:
                    ranks = [i for i in rdic[key] if i in list(combdic[key][:30])] 
                    sp += float(len([j for j in ranks[:topK] if avglist[list(combdic.keys()).index(key)][list(combdic[key][:30]).index(j)] == 1])/topK)
                temK_list.append(sp/len(keys))
            sp_list.append(temK_list)
        print(sp_list)

    elif MODE == 'MAP':
        map_list = []
        for rdic in dics:
            smap = 0.0
            for key in keys:
                ranks = [i for i in rdic[key] if i in list(combdic[key][:30])] 
                rels = [ranks.index(i) for i in ranks if avglist[list(combdic.keys()).index(key)][list(combdic[key][:30]).index(i)] == 1]
                tem_map = 0.0
                for rel_rank in rels:
                    tem_map += float(len([j for j in ranks[:rel_rank+1] if avglist[list(combdic.keys()).index(key)][list(combdic[key][:30]).index(j)] == 1])/(rel_rank+1))
                if len(rels) > 0:
                    smap += tem_map / len(rels)
            map_list.append(smap/len(keys))
        print(map_list)
    
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
    #             pre = float(len([j for j in ranks[:topK] if avglist[k][list(combdic[key][:30]).index(j)] == 1])/topK)
    #             allrel = len([j for j in ranks[:] if avglist[k][list(combdic[key][:30]).index(j)] == 1])
    #             if allrel > 0 and pre > 0:
    #                 recall = float(len([j for j in ranks[:topK] if avglist[k][list(combdic[key][:30]).index(j)] == 1])/allrel)
    #                 sf1 += 2/(1/pre+1/recall)
    #             k += 1
    #         f1_list.append(sf1/100)

    #     print(f1_list)
    

