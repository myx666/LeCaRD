# LeCaRD: A Chinese Legal Case Retrieval Dataset 
![GitHub](https://img.shields.io/github/license/myx666/LeCaRD) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/numpy)

## Overview
* [Background](#background)

- [Dataset Structure](#dataset-structure)

- [Install](#install)

- [Usage](#usage)
	- [query.json](#queryjson)
	- [candidates](#candidates)
	- [golden_labels.json](#golden_labelsjson)

- [Evaluation](#evaluation)

- [Experiment](#experiment)

- [Citation](#citation)

- [Authors](#authors)

- [License](#license)

## Background

The **Le**gal **Ca**se **R**etrieval **D**ataset (**LeCaRD**) contains 107 query cases and 10,700 candidate cases. Queries and results are adopted from criminal cases published by [the Supreme People’s Court of China](https://wenshu.court.gov.cn/). Relevance judgments criteria and annotation are all conducted by our legal expert team. For dataset evaluation, we implemented several existing retrieval models on LeCaRD as baselines. 

## Dataset Structure

`/LeCaRD/data` is the root directory of all LeCaRD data. The meanings of some main files (or directories) are introduced below: 

```
data
├── candidates                       
│   ├── candidates1.zip			// [important] candidate zipfile 1(for query 1-50)
│   └── candidates2.zip			// [important] candidate zipfile 2(for query 51-107)
├── corpus
│   ├── common_charge.json
│   ├── controversial_charge.json
│   └── document_path.json		// corpus document path file
├── label
│   ├── golden_labels.json		// [important] golden labels for candidates
│   └── label_top30.json		// labels of top 30-relevant candidates
├── others
│   ├── criminal charges.txt		// list of all Chinese criminal charges
│   └── stopword.txt
├── prediction				// candidate pooling results using different methods
│   ├── bert.json
│   ├── bm25_top100.json
│   ├── combined_top100.json		// overall candidate list
│   ├── lm_top100.json
│   └── tfidf_top100.json
└── query
    └── query.json			// [important] overall query file

6 directories, 15 files
```

## Install
1. Clone the project
2. To utilize queries and the corresponding candidates, unzip the candidate file:

```bash
$ cd YOUR-LOCAL-PROJECT-PATH/LeCaRD
$ unzip data/candidates/candidates1.zip -d data/candidates
$ unzip data/candidates/candidates2.zip -d data/candidates
```
3. (Optional) All queries and candidates are selected from a corpus containing over 43,000 Chinese criminal documents. If you are interested, download the corpus zipfile through [this link](https://drive.google.com/file/d/1vQdX1MegFVtmoh0XCd4mav5PBkep7q0h/view?usp=sharing).

4. (Optional) Corpus_jieba.json used in our paper: [this link](https://drive.google.com/file/d/1vQdX1MegFVtmoh0XCd4mav5PBkep7q0h/view?usp=sharing)

5. Get started!

## Usage

For a quick start, you only need to get familiar with three files (also marked as [important] in [Dataset Structure](#dataset-structure)): `query.json`, `candidates`, and `golden_labels.json
`. 

### query.json
`query.json` has 107 lines. Each line is a *dictionary* representing a query. An example of a *dictionary* is: 

> {"path": "ba1a0b37-3271-487a-a00e-e16abdca7d83/005da2e9359b1d71ae503d98fba4d3f31b1.json", "ridx": 1325, "q": "2016年12月15日12时许，被害人郑某在台江区交通路工商银行自助ATM取款机上取款后，离开时忘记将遗留在ATM机中的其所有的卡号为62×××73的银行卡取走。后被告人江忠取钱时发现该卡处于已输入密码的交易状态下，遂分三笔取走卡内存款合计人民币（币种，下同）6500元。案发后，被告人江忠返还被害人郑某6500元并取得谅解。", "crime": ["诈骗罪", "信用卡诈骗罪"]}

where `path` is the path of query's full text in [the corpus](https://drive.google.com/file/d/1vQdX1MegFVtmoh0XCd4mav5PBkep7q0h/view?usp=sharing), `ridx` is each query's unique ID, `q` is the query content, and `crime` is the criminal charge(s) of this query case.

### candidates

`candidates` directory contains 107 subdirectories, each of which consists of 100 candidate documents. An example of a candidate documents is:

> {"ajId":"dee49560-26b8-441b-81a0-6ea9696e92a8","ajName":"程某某走私、贩卖、运输、制造毒品一案","ajjbqk":" 公诉机关指控，2018年3月1日下午3时许，被告人程某某在本市东西湖区某某路某某工业园某某宾馆门口以人民币300元的价格向吸毒人员张某贩卖毒品甲基苯丙胺片剂5颗......","pjjg":" 一、被告人程某某犯贩卖毒品罪，判处有期徒刑十个月......","qw":"湖北省武汉市东西湖区人民法院 刑事判决书 （2018）鄂0112刑初298号 公诉机关武汉市东西湖区人民检察院。 被告人程某某......","writId": "0198ec7627d2c78f51e5e7e3862b6c19e42", "writName": "程某某走私、贩卖、运输、制造毒品一审刑事判决书"}

where `ajId` is the ID of the case, `ajName` is the case name, `ajjbqk` is the basic facts of the case, `pjjg` is the case judgment, `qw` is the full content, `writId` is the unique ID of this document, and `writName` is the document name.

### golden_labels.json

`golden_labels.json` is formulated in the following manner:

> { ridx_1: [rel_11, rel_12, ...], ridx_2: [rel_21, rel_22, ...], ... }

where `key` is the query ID and `value` is a list of query's relevant case IDs. The number of relevant cases depends on its corresponding query. 

## Evaluation

`metrics.py` is an demo program of evaluating your own model predictions on LeCaRD. The usage of `metrics.py` is:

```bash
$ cd YOUR-LOCAL-PROJECT-PATH/LeCaRD
$ python metrics.py --help

usage: metrics.py [-h] [--m {NDCG,P,MAP}] [--label LABEL] [--pred PRED]
                  [--q {all,common,controversial,test}]

Help info:

optional arguments:
  -h, --help            show this help message and exit
  --m {NDCG,P,MAP}      Metric.
  --label LABEL         Label file path.
  --pred PRED           Prediction dir path.
  --q {all,common,controversial,test}
                        query set
```

Your own model prediction file must has the same format as files in `/data/prediction`, where the files have query IDs as keys and their corresponding candidate ranking lists as values in a dictionary.

## Experiment

We implemented three traditional retrieval models (BM25, TF-IDF, and Language Models) and BERT as baselines for the evaluation on LeCaRD's top 30-relevant candiates.

For traditional models, we first test their performances on the overall (common + controversial) query set. All traditional models are trained on [the corpus](https://drive.google.com/file/d/1vQdX1MegFVtmoh0XCd4mav5PBkep7q0h/view?usp=sharing). The results are:

| **Model** | **P@5** | **P@10** | **MAP** | **NDCG@10** | **NDCG@20** | **NDCG@30** | 
|:----------|:----------|:----------|:----------|:----------|:----------|:----------|
| BM25   | 0.406    | 0.381    | 0.484    | 0.731    | 0.797    | 0.888    |
| TF-IDF | 0.304    | 0.261    | 0.457    | **0.795**    | **0.832**    | 0.848    |
| LMIR   | **0.436**    | **0.406**    | **0.495**    | 0.769    | 0.818    | **0.900**    |

In terms of the pre-trained model, we adopt a criminal law-specific BERT published by [THUNLP](https://github.com/thunlp/openclap), which was pre-trained by 663 million Chinese criminal judgments. The fine-tuned BERT is evaluated on the overall query set with a test-train split together with BM25, TF-IDF, and Language Models for comparison. The results are:

| **Model** | **P@5** | **P@10** | **MAP** | **NDCG@10** | **NDCG@20** | **NDCG@30** |
|:----------|:----------|:----------|:----------|:----------|:----------|:----------|
| BM25    | 0.380    | 0.350    | 0.498    | 0.739    | 0.804    | 0.894    |
| TF-IDF  | 0.270    | 0.215    | 0.459    | **0.817**    | **0.836**    | 0.853    |
| LMIR    | 0.450    | **0.435**    | 0.512    | 0.769    | 0.807    | 0.896    |
| BERT    | **0.470**    | 0.430    | **0.568**    | 0.774    | 0.821    | **0.899**    |

## Citation
```
@article{ma2021lecard,
  title={LeCaRD: A Legal Case Retrieval Dataset for Chinese Law System},
  author={Ma, Yixiao and Shao, Yunqiu and Wu, Yueyue and Liu, Yiqun and Zhang, Ruizhe and Zhang, Min and Ma, Shaoping},
  journal={Information Retrieval (IR)},
  volume={2},
  pages={22},
  year={2021}
}
```

## Authors

Yixiao Ma(myx666) mayx20@mails.tsinghua.edu.cn \
Yunqiu Shao  shaoyunqiu14@gmail.com \
Yueyue Wu wuyueyue1600@gmail.com \
Yiqun Liu yiqunliu@tsinghua.edu.cn \
Ruizhe Zhang u@thusaac.com \
Min Zhang z-m@tsinghua.edu.cn \
Shaoping Ma msp@tsinghua.edu.cn 

## License

[MIT](LICENSE) © Yixiao Ma

