import os.path
import json

from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()

def lemmatize(word):
    token = word.strip()
    token = morph.normal_forms(token)[0]
    return token

def find_docs_contains(word):
    with open('inverse_idx.json') as json_file:
        inverse_idx = json.load(json_file)
    try:
        if word.startswith('!'):
            return [page for k,v in inverse_idx.items() if k != lemmatize(word[1:]) for page in v ]
        else:
            return inverse_idx[lemmatize(word)]
    except Exception as e:
        print("Word not found: %s" % e)


if __name__ == "__main__":
    result = []
    req = input()
    sub_req_or = req.split('|')
    for sub_or in sub_req_or:
        sub_or = sub_or.strip()
        if '&' in sub_or:
            sub_req_and = sub_or.split('&')
            intersect = set([])
            for idx, sub_and in enumerate(sub_req_and):
                sub_and = sub_and.strip()
                docs = find_docs_contains(word=sub_and)
                if idx == 0:
                    intersect |= set(docs)
                else:
                    intersect = set.intersection(intersect, set(docs))
            docs = list(intersect)
        else:
            docs = find_docs_contains(word=sub_or)
        result += docs
    result = sorted(set(result))
    print(result)
