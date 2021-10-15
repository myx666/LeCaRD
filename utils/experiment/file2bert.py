# -*- encoding: utf-8 -*-
'''
@Func    :   transfer file to bert-readable style
@Time    :   2021/03/04 17:36:47
@Author  :   Yixiao Ma 
@Contact :   mayx20@mails.tsinghua.edu.cn
'''

import os
import re
import numpy as np
import json
import argparse
from tqdm import tqdm
import sys
sys.path.append('/work/mayixiao/www22/')
from pre_ajjbqk import process_ajjbqk

parser = argparse.ArgumentParser(description="Help info.")
parser.add_argument('--short', type=bool, default=False, help='if pre ajjbqk.')
parser.add_argument('--w', type=str, default='/work/mayixiao/www22/', help='Write file path.')

# parser.add_argument('--mode', type=str, choices=['train', 'test'], help='mode.')
# parser.add_argument('--l', type=str, default='/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/label/label_top30_dict.json', help='Label file path.')
# parser.add_argument('--q', type=str, default='/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/query/query.json', help='Query file path.')
# parser.add_argument('--d', type=str, default='/work/mayixiao/similar_case/candidates', help='Document dir path.')
# cpfxgc_dic = json.load(open('/work/mayixiao/www22/extracted_cpfxgc.json', 'r'))

parser.add_argument('--mode', type=str, choices=['train_2', 'test_2'], help='mode.')
parser.add_argument('--l', type=str, default='/work/mayixiao/similar_case/202006/data/label/label_top30_dict_2.json', help='Label file path.')
parser.add_argument('--q', type=str, default='/work/mayixiao/similar_case/202006/data/query/', help='Query file path.')
parser.add_argument('--d', type=str, default='/work/mayixiao/similar_case/202006/data/candidates_2', help='Document dir path.')
cpfxgc_dic = json.load(open('/work/mayixiao/www22/extracted_cpfxgc_2.json', 'r'))

args = parser.parse_args()

w_list = []

if args.mode == 'train' or args.mode == 'test':
    with open(args.q, 'r') as f:
        lines = f.readlines()
        if args.mode == 'train':
            lines = [line for line in lines if (lines.index(line)%5 != 0 or lines.index(line)>=100)]
        elif args.mode == 'test':
            lines = [line for line in lines if (lines.index(line)%5 == 0 and lines.index(line)<100)]
        else:
            raise NotImplementedError
else:
    name_map = {'train_2':'query2_final.json', 'test_2':'query2_big.json'}
    lines = open(args.q + name_map[args.mode], 'r').readlines()

with open(args.l, 'r') as f:
    labels = json.load(f)


raw_c_list = open('/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/others/criminal charges.txt', 'r').readlines()
c_list = [c[:-1] for c in raw_c_list[:-1]]
c_list.append(raw_c_list[-1])

def make_data(dic, qid, cid, cls=2):
    tem = {}
    tem['guid'] = qid + '_' + cid
    tem['text_a'] = dic['q']
    c_dic = json.load(open(os.path.join(args.d, qid, cid+'.json'), 'r'))
    if 'pjjg' in c_dic:
        c_doc = c_dic['pjjg']
    else:
        c_doc = c_dic['ajjbqk']
    if args.short:
        tem['text_b'] = process_ajjbqk(c_dic['ajjbqk'])
    else:
        tem['text_b'] = c_dic['ajjbqk']
    
    if cid in cpfxgc_dic:
        tem['text_c'] = cpfxgc_dic[cid]
    else: 
        tem['text_c'] = []
    tem['c_a'] = dic['crime']
    tem['c_b'] = []
    for crime in c_list:
        if crime in c_doc:
            idx = c_doc.index(crime)
            if crime == '侵占罪' and c_doc[idx-2: idx] == '职务':
                continue
            if crime == '受贿罪' and ( c_doc[idx-2: idx] == '单位' or c_doc[idx-5: idx] == '利用影响力' or c_doc[idx-7: idx] == '非国家工作人员' ):
                continue
            if crime == '行贿罪' and ( c_doc[idx-2: idx] == '单位' or c_doc[idx-3: idx] == '对单位' or c_doc[idx-7: idx] == '对有影响力的人' or c_doc[idx-8: idx] == '对非国家工作人员' or c_doc[idx-16: idx] == '对外国公职人员、国际公共组织官员'):
                continue
            tem['c_b'].append(crime)
    if '走私、贩卖、运输、制造毒品罪' not in tem['c_b']:
        tem_c_list = ['走私毒品罪', '贩卖毒品罪', '运输毒品罪', '制造毒品罪', '走私、贩卖毒品罪', '走私、运输毒品罪', '走私、制造毒品罪', '贩卖、运输毒品罪', '贩卖、制造毒品罪', '运输、制造毒品罪', '贩卖、运输、制造毒品罪', '走私、运输、制造毒品罪', '走私、贩卖、制造毒品罪', '走私、贩卖、运输毒品罪']
        for crime in tem_c_list:
            if crime in c_doc and '走私、贩卖、运输、制造毒品罪' not in tem['c_b']:
                tem['c_b'].append('走私、贩卖、运输、制造毒品罪')
    if '非法持有、私藏枪支、弹药罪' not in tem['c_b']:
        tem_c_list = ['非法持有枪支、弹药罪', '非法持有枪支罪', '非法持有弹药罪', '非法私藏枪支、弹药罪', '非法私藏枪支罪', '非法私藏弹药罪', '非法持有、私藏枪支罪', '非法持有、私藏弹药罪']
        for crime in tem_c_list:
            if crime in c_doc and '非法持有、私藏枪支、弹药罪' not in tem['c_b']:
                tem['c_b'].append('非法持有、私藏枪支、弹药罪')
    
    if cls == 2:
        if cid in labels[qid]:
            if labels[qid][cid] >= 2:
                tem['label'] = 1 
            else:
                tem['label'] = 0
        else:
            tem['label'] = 0

    elif cls == 4:
        if cid in labels[qid]:
            tem['label'] = labels[qid][cid]
        else:
            tem['label'] = 0

    return tem

max_len = 0
for line in tqdm(lines):
    dic = eval(line)
    qid = str(dic['ridx'])
    pos_num = 0
    # l0_num = 0
    for cid in labels[qid]:
        tem = make_data(dic, qid, cid, 2)
        w_list.append(tem)
        if tem['label'] == 1:
            pos_num += 1
        # elif tem['label'] == 0:
        #     l0_num += 1
        max_len = max(max_len, len(tem['text_a']) + len(tem['text_b']))
    if args.mode[:4] != 'test' and pos_num > 15:
        delta = 2*pos_num - 30
        files = os.listdir(os.path.join(args.d, qid))
        cids = [file_.split('.')[0] for file_ in files if file_.split('.')[0] not in labels[qid]][:delta]
        for cid in cids:
            tem = make_data(dic, qid, cid, 2)
            w_list.append(tem)
            max_len = max(max_len, len(tem['text_a']) + len(tem['text_b']))

if args.short:
    tail = '_short.json'
else:
    tail = '.json'
# if args.short:
#     tail = '_short_4cls.json'
# else:
#     tail = '_4cls.json'

with open(args.w + args.mode + tail, 'w') as f:
    for line in w_list[:-1]:
        json.dump(line, f, ensure_ascii=False)
        f.write('\n')
    json.dump(w_list[-1], f, ensure_ascii=False)

print(max_len)