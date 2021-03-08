import os
import json
from tqdm import tqdm
from shutil import copytree

with open('/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/corpus/document_path.json', 'r') as f:
    paths = json.load(f)

root = '/work/yangjun/LAW/preprocess_new_data/feature_data'

singles = paths['single']
retrials = paths['retrial']

# for p in singles:
#     copytree(os.path.join(root, p.split('/')[0]), '/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/corpus/documents/'+p.split('/')[0])

for p in tqdm(retrials):
    copytree(os.path.join(root, p[0].split('/')[0]), '/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/corpus/documents/'+p[0].split('/')[0])

# copytree('/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/label', 'testlabel')

# with open('/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/prediction/combined_top100.json', 'r') as f:
#     cmbfile = json.load(f)

# with open('/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/label/label_top30.json', 'r') as f:
#     labelfile = json.load(f)[3]

# keys = list(cmbfile.keys())

# w_dict = {}

# for key in keys[:100]:
#     indexs = [i for i in range(30) if labelfile[key][i] == 1]
#     w_dict[key] = [cmbfile[key][j] for j in indexs]

# with open('/work/mayixiao/similar_case/LeCaRD/LeCaRD_github/data/label/golden_labels.json','w') as f:
#     json.dump(w_dict,f, ensure_ascii=False)
