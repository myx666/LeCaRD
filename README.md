# LeCaRD: A Chinese Legal Case Retrieval Dataset ![GitHub](https://img.shields.io/github/license/myx666/LeCaRD) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/numpy)

## Overview
* [Background](#background)

- [Install](#install)

- [Usage](#usage)


## Background

The **Le**gal **Ca**se **R**etrieval **D**ataset (**LeCaRD**) contains 106 query cases and over 43,000 candidate cases. Queries and results are adopted from criminal cases published by [the Supreme People’s Court of China](https://wenshu.court.gov.cn/). Relevance judgments criteria and annotation are all conducted by our legal expert team. For dataset evaluation, we implemented several existing retrieval models on LeCaRD as baselines. 

## Project Structure

`/LeCaRD/data` is the root directory of all LeCaRD data. The meanings of some main files (or directories) are introduced below: 

```
data
├── candidates                       
│   └── candidates.zip			// [important] candidates zipfile
├── corpus
│   ├── common_charge.json
│   ├── controversial_charge.json
│   └── document_path.json
├── label
│   ├── golden_labels.json		// [important] golden labels for candidates
│   └── label_top30.json		// labels of top 30-relevant candidates
├── others
│   ├── criminal charges.txt		// list of all Chinese criminal charges
│   └── stopword.txt
├── prediction
│   ├── bert.json
│   ├── bm25_top100.json
│   ├── combined_top100.json		// overall candidate list
│   ├── lm_top100.json
│   └── tfidf_top100.json
└── query
    ├── common_query.json
    ├── controversial_query.json
    └── query.json			// [important] overall query file

6 directories, 16 files

```

## Install
1. Clone the project
2. To utilize queries and corresponding candidates, unzip the candidate file:

```
$ cd YOUR-LOCAL-PROJECT-PATH/LeCaRD
$ unzip data/candidates/candidates.zip -d data/candidates
```
3. (Optional) All queries and candidates are selected from a corpus containing over 43,000 Chinese criminal documents. If you are interested, download the corpus zipfile through [this link](https://drive.google.com/file/d/1vQdX1MegFVtmoh0XCd4mav5PBkep7q0h/view?usp=sharing).

4. Get started!

## Usage

## License

[MIT](LICENSE) © Yixiao Ma

