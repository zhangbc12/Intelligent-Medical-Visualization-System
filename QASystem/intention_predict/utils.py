import pandas as pd
import numpy as np

def load_txt(file):
    with  open(file,encoding='utf-8',errors='ignore') as fp:
        lines = fp.readlines()
        lines = [l.strip() for l in lines]
        print("Load data from file (%s) finished !"%file)
    return lines

def load_vocabulary(file_vocabulary_label):
    """
    Load vocabulary to dict
    """
    vocabulary = load_txt(file_vocabulary_label)
    dict_id2label,dict_label2id = {},{}
    for i,l in enumerate(vocabulary):
        dict_id2label[str(i)] = str(l)
        dict_label2id[str(l)] = str(i)
    return dict_id2label,dict_label2id

def load_csv(file,encoding='utf-8',header=0):
    return pd.read_csv(file,encoding=encoding,header=header,error_bad_lines=False)#,encoding='gbk'

def shuffle_one(a1):
    ran = np.arange(len(a1))
    np.random.shuffle(ran)
    return np.array(a1)[ran].tolist()
