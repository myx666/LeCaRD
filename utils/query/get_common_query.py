# -*- encoding: utf-8 -*-
'''
@Func    :   get common queries from ridx
@Time    :   2021/03/05 11:02:03
@Author  :   Yixiao Ma 
@Contact :   mayx20@mails.tsinghua.edu.cn
'''

import os
import re
import json
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Help info.")
parser.add_argument('--c', type=str, default='data/corpus', help='Corpus dir path.')
parser.add_argument('--fact', type=str, default='data/others/fact_content.json', help='Fact content path.')
parser.add_argument('--w', type=str, default='data/query/common_query.json', help='Write path.')

args = parser.parse_args()

with open (os.path.join(args.c, 'document_path.json'),'r') as f:
    jsfile = json.load(f)

with open (os.path.join(args.c, 'common_charge.json'),'r') as g:
    labels = json.load(g)

with open (args.fact, 'r') as h:
    # facts = json.load(h)
    facts = h.readlines()

wjson = [] # {"ridx":,"id":,"crime":[],"q":}
ridxs = [
5156,	4891,	4900,	5187,
330,	706,	259,	221,
2132,	2143,	1972,	1978,
2361,	2373,	2331,
3228,	3746,	3765,	3342,
1405,	1430,	1325,	1355,
4738,	4794,	4829,	4719,
883,	836,	837,	861,
3952,	3878,	3943,	4023,
5511,	5478,	5504,	5561,
2174,	2198,	2186,	2203,
5193,	5239,	5223,	5214,
6905,	6909,	6917,
3805,	3817,	3814,	3862,
6820,	6775,	6816,
6706,	6700,	6670,	6652,
2403,	2387,	2430,	2401,
6394,	6432,	6409,	6282,
4852,	4873,	4863,	4847,
6094,	6072,	6046,	6081 ]

paths = jsfile['single']

rds = []
ids = []

for ridx in tqdm(ridxs[:]):
    temfact = ''
    for dic in facts:
        dic = eval(dic)
        if dic["ridx"] == ridx:
            temfact = dic["fact"]
    for path in paths:
        with open (os.path.join(ROOT,path),'r') as f:
            case = json.load(f)
        if "ajjbqk" in case:
            temstr = case["ajjbqk"].replace( ' ' , '' )
            if temfact in temstr:
                temdic = {}
                temdic['path'] = path
                temdic['ridx'] = ridx
                temdic['jbqk'] = temfact
                temdic['fxgc'] = case['cpfxgc']
                temdic['crime'] = []

                for key in labels:
                    if path in labels[key]:
                        temdic['crime'].append(key)
                wjson.append(temdic)
                pass
                # print(os.path.join(ROOT,path))

with open(args.w, 'w') as f:
    for i in wjson:
        json.dump(i, f, ensure_ascii=False)
        # f.write('\n')
    # json.dump(wjson, f, ensure_ascii=False)
       