# 从excel获取标注结果

import os
import xlrd
import json
from tqdm import tqdm
import numpy as np

L_ROOT = '/work/mayixiao/similar_case/LeCaRD/label'
files = [['part1.xlsx', 'part2.xlsx', 'part3--程睿标注.xlsx'],
            ['part1 (1).xlsx', 'part2完.xlsx', '类案标注3.part3.xlsx'],
                ['1-辛佳东-法大.xlsx', '2_part2(1).xlsx', '3-中共中央党校-郭坤旭.xlsx']]
bert_files = ['/work/mayixiao/coliee_2020/coliee20_pytorch_worker/result/LeCaRD1.json', '/work/mayixiao/coliee_2020/coliee20_pytorch_worker/result/LeCaRD2.json', '/work/mayixiao/coliee_2020/coliee20_pytorch_worker/result/LeCaRD3.json', '/work/mayixiao/coliee_2020/coliee20_pytorch_worker/result/LeCaRD4.json']
W_PATH = '/work/mayixiao/similar_case/LeCaRD/label/label.json'

wjson = []
for i in range(3):
    temlist = []
    for j in range(3):
        data = xlrd.open_workbook(os.path.join(L_ROOT,files[i][j]))
        for k in range(j*33+1,j*33+34):
            table = data.sheet_by_name(str(k))
            temlist.append(table.col_values(2)[1:])
        if j == 2:
            table = data.sheet_by_name(str(100))
            temlist.append(table.col_values(2)[1:])
    wjson.append(temlist)
    print(len(temlist))

avglist = []
for i in range(100):
    temlist = []
    for j in range(30):
        tem = 0
        for k in range(3):
            tem += wjson[k][i][j]
        if tem <= 4:
            temlist.append(1)
        elif tem > 4 and tem <= 7:
            temlist.append(2)
        elif tem > 7 and tem <= 10:
            temlist.append(3)
        elif tem > 10 and tem <= 12:
            temlist.append(4)
    
    avglist.append(temlist)
wjson.append(avglist)

# read predictions from BERT 

with open('/work/mayixiao/similar_case/combined_top100.json','r') as f:
    combdic = json.load(f)

dicts = []
for bfile in bert_files[:]:
    bert_dict = {}
    with open(bfile, 'r') as f:
        lines = f.readlines()

    tem_dict= {}
    for line in lines[:]:
        tem_dict[eval(line)['id_'].split('_')[1]] = eval(line)['res']
        if lines.index(line) % 30 == 29:
            key = eval(line)['id_'].split('_')[0]
            bert_dict[key] = [combdic[key][int(i)] for i,j in sorted(tem_dict.items(), key = lambda case: case[1][1]-case[1][0], reverse=True)]
            # print(bert_dict)
    dicts.append(bert_dict)

with open('/work/mayixiao/similar_case/LeCaRD/label/bert.json' ,'w') as f:
    for line in dicts:
        json.dump(line,f, ensure_ascii=False)
        f.write('\n')
        
with open(W_PATH,'w') as f:
    json.dump(wjson, f, ensure_ascii=False)


