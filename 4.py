from collections import defaultdict
import os, os.path
import re
import json
import math
from math import log
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords

patterns = "[!#$%&'()*+,.«»/+:;\-<=>?@©\n\t\r[\]^_`{|}~—\"\\\x0b\x0c]"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()

def get_tf(text):
    text = re.sub(patterns, ' ', text)
    tf = defaultdict(float)
    for token in text.split():
        if not token or token in stopwords_ru:
            continue
        token = token.strip()
        token = morph.normal_forms(token)[0]
        tf[token] += 1
    for word, count in tf.items():
        tf[word] = count / len(text.split())
    return tf

def get_docs(dir):
    return [name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name)) and name != 'index.txt']

# TF - количество употребления слова по отношению ко всем словам в документе
def get_tf_docs():
    tf_docs = {}
    docs = get_docs('./1')
    for doc in docs:
        with open(f'./1/{doc}', 'r') as f:
            text = f.read()
        try:
            tf_docs[doc] = get_tf(text)
        except Exception as e:
            print(e)
            continue
    return tf_docs

# IDF - log(количество документов / количество документов с вхождением слова)
def get_idf(inverse_idx):
    idf = dict()
    PAGES_COUNT = len(get_docs('./1'))
    for word in inverse_idx:
        doc_count = len(inverse_idx[word])
        idf[word] = log(PAGES_COUNT / doc_count)
    return idf

# TF-IDF = TF * IDF
def get_tf_idf(tf, idf):
    tf_idf = dict()
    for word, tf_value in tf.items():
        tf_idf[word] = tf_value * idf[word]
    return tf_idf

if __name__ == '__main__':
    with open('./inverse_idx.json', 'r') as f:
        inverse_idx = json.load(f)

    docs_tf = get_tf_docs()
    docs_idf = get_idf(inverse_idx)
    docs_tf_idf = {}
    for doc, doc_tf in docs_tf.items():
        docs_tf_idf[doc] = get_tf_idf(doc_tf, docs_idf)

    for doc, doc_tf in docs_tf.items():
        with open(f'./tf_idf/{doc}', 'a') as f:
            f.write('word tf tf_idf\n')
            for word, tf in doc_tf.items():
                f.write(f'{word} {round(tf, 6)} {round(docs_tf_idf[doc][word], 6)}\n')
    
    with open('./idf.txt', 'a') as f:
        f.write('word idf\n')
        for word, idf in docs_idf.items():
            f.write(f'{word} {round(idf, 6)}\n')
    
    # for doc, doc_tf_idf in docs_tf_idf:
    #     with open(f'./tf_idf/{doc}', 'a') as f:
    #         f.write(f'word tf_idf')
