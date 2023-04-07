import os, os.path
import re
import json
import math

from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords

patterns = "[!#$%&'()*+,.«»/+:;\-<=>?@©\n\t\r[\]^_`{|}~—\"\\\x0b\x0c]"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()
docs_dir = './1'
with open('./inverse_idx.json', 'r') as f:
    inverse_idx = json.load(f)

def get_docs(dir):
    return [name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name)) and name != 'index.txt']

def get_tokens(text):
    text = re.sub(patterns, ' ', text)
    tokens = []
    for token in text.split():
        if not token or token in stopwords_ru:
            continue
        token = token.strip()
        token = morph.normal_forms(token)[0]
        tokens.append(token.lower())
    return tokens

def get_tf_idf(words):
    tf_idf = {}
    for w in words:
        tf = sum(w in w1 for w1 in words)/len(words)
        PAGES_COUNT = len(get_docs(docs_dir))
        try:
            idf = math.log(PAGES_COUNT / len(inverse_idx[w]))
        except:
            idf = 0 
        tf_idf[w] = tf * idf
    
    return tf_idf

def get_docs_tf_idf(words):
    docs_vector = {}
    for doc_name in get_docs(docs_dir):
        with open(f'./tf_idf/{doc_name}', 'r') as f:
            tf_idf = {l.split()[0]: l.split()[-1] for l in f.readlines()[1:]}

        docs_vector[doc_name] = [tf_idf.get(w, 0.0) for w in words]

    return docs_vector

def get_vector_length(vec):
    return math.sqrt(sum(float(i)**2 for i in vec))

def get_cosin(vec1, vec2):
    if len(vec1) != len(vec2):
        raise(f'Cannot get cosin of unequal size of vectors: \n{vec1}\n{vec2}\n')
    dist1 = get_vector_length(vec1)
    dist2 = get_vector_length(vec2)
    if dist1 == 0 or dist2 == 0:
        return 0
    return sum([float(v1) * float(v2) for v1, v2 in zip(vec1,vec2)]) / (dist1 * dist2)

def get_cosin_distances(query_vector, docs_vector):
    distances = {}
    for doc_name, doc_vector in docs_vector.items():
        cosin = get_cosin(query_vector, doc_vector)
        distances[doc_name] = cosin
    
    return distances


def search(query, threshold):
    words = get_tokens(query)
    query_tf_idf_vector = get_tf_idf(words)
    docs_tf_idf_vector = get_docs_tf_idf([w for w in query_tf_idf_vector])
    distances = get_cosin_distances([float(v) for k,v in query_tf_idf_vector.items()], docs_tf_idf_vector)
    searched_indices = sorted(distances.items(), key=lambda x: x[1], reverse=True)
    return [(doc,dist) for doc, dist in searched_indices if dist > threshold]

if __name__ == '__main__':
    query = input()
    searched_indices = search(query, 0.05)
    for idx in searched_indices:
        print(idx)
