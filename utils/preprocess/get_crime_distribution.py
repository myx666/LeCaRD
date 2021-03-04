import re
import tqdm
import os
import json

CRIMEPATH = './crimepath.json'
CHARGEPATH = './criminal charges.txt'
CASE_ROOT = '/work/yangjun/LAW/preprocess_new_data/feature_data'
# LABELPATH = './chargelabel.json'
# LABELPATH = './retriallabel.json'
charges = []
ans = {}
with open(CRIMEPATH, 'r') as f:
    jspath = json.load(f)

with open(CHARGEPATH, 'r') as k:
    lines = k.readlines()

res = [re.compile(line[:-2]) for line in lines]
count = 0
# count2 = 0
for path in jspath['single'][:]:
    # for path in paths:
    fullpath = os.path.join(CASE_ROOT, path)
    with open(fullpath, 'r') as g:
        file_ = json.load(g)
    flag = 0
    for crime in res:
        if crime.search(file_['writName']):
            charge = crime.search(file_['writName']).group()+'罪'
            # count2 += 1
            if charge in ans:
                ans[charge].append(path)
            else:
                ans[charge] = [path]
            flag = 1
    if flag == 0:
        print(fullpath)
        count += 1


print(count)
print(sum([len(ans[i]) for i in ans.keys()]))
with open(LABELPATH, 'a') as h:
    json.dump(ans, h, ensure_ascii=False)

print(len(ans.keys()))
# if __name__ == "__main__":
#     a = ['是是是','s得到']
    # for i in a:
    #     isa = re.compile(i[:-1])
    #     print(isa.search('嗯嗯嗯是2145是'))
    # s = {}
    # s['e'].append(1)
    # print(s)
    
