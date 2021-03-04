import os
import re
import numpy as np
import json
from tqdm import tqdm

WRITEPATH = '/work/mayixiao/similar_case/crimepath.json'
CASE_ROOT = '/work/yangjun/LAW/preprocess_new_data/feature_data'
iscriminal = re.compile(r'.*罪.*')
isverdict = re.compile(r'.*刑事判决书.*')
raw_dirs = os.listdir(CASE_ROOT)
dirs = [dir_ for dir_ in raw_dirs if os.path.isdir(os.path.join(CASE_ROOT, dir_))]
jspaths = {'single':[],'retrial':[]} #刑事案件判决书的路径、有再审判决书的路径

# print(len(dirs), dirs[:10])

for dir in tqdm(dirs[:]):
    dirpath = os.path.join(CASE_ROOT, dir)
    if os.path.isdir(dirpath):
        files = [_file for _file in os.listdir(dirpath) if os.path.isdir(dirpath) and os.path.isfile(os.path.join(dirpath, _file))]
    tem_retrival = []
    # with open(os.path.join(dirpath,files[0]), 'r') as f: # 检验相同案件下文书名称是否相同
    #     jsfile = json.load(f)
    #     if 'ajName' in jsfile:
    #         name = jsfile['ajName']
    #     else:
    #         print('no ajName: ', os.path.join(dirpath,files[0]))
    for file_ in files:
        with open(os.path.join(dirpath,file_), 'r') as f:
            jsfile = json.load(f)
        
        if 'ajjbqk' in jsfile:
            if 'writName' in jsfile:
                if isverdict.match(jsfile['writName']):
                    tem_retrival.append(os.path.join(dir,file_))
            # elif 'ajName' in jsfile and iscriminal.match(jsfile['ajName']):
                # print('no writName: ', os.path.join(CASE_ROOT,dir,file_))

    if len(tem_retrival) == 1:
        jspaths['single'].append(tem_retrival[0])
    elif len(tem_retrival) > 1:
        jspaths['retrial'].append(tem_retrival)

# print(jspaths)
with open(WRITEPATH,'w') as g:
    json.dump(jspaths, g, ensure_ascii=False)

print(len(jspaths['single']), len(jspaths['retrial']))
# if __name__ == "__main__":
#     a = {'a':1,'b':2}
#     print('a' in a)
    # iscriminal = re.compile(r'.*罪.*')
    # print(iscriminal.match('爆炸物罪一案').group())