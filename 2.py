import os, os.path
import re
import json

from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@©\n\t\r[\]^_`{|}~—\"\\\-]+"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()

def lemmatize(text):
    text = re.sub(patterns, ' ', text)
    tokens = []
    for token in text.split():
        if not token or token in stopwords_ru:
            continue
        token = token.strip()
        token = morph.normal_forms(token)[0]
        tokens.append(token)
    if len(tokens) > 2:
        return set(tokens)
    return None

dir = './2023-03-04 08:01:54.701845'

if __name__ == '__main__':
    files = [name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name)) and name != 'index.txt']
    inverse_idx = {}
    for file_name in files:
        with open(dir + '/' + file_name, 'r') as f:
            text = f.read()
        try:
            tokens = lemmatize(text)
        except Exception as e:
            print(e)
            continue
        for t in tokens:
            if t not in inverse_idx:
                inverse_idx[t] = [file_name]
            else:
                inverse_idx[t].append(file_name)
    with open('./inverse_idx.json', 'w+') as fp:
        json.dump(inverse_idx, fp)

        