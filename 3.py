import json

def find_docs_contains(word):
    with open('inverse_idx.json') as json_file:
        inverse_idx = json.load(json_file)
    result = []
    if word.startswith('!'):
        return [page for k,v in inverse_idx if k != word[1:] for page in v ]
    else:
        return inverse_idx[word]

if __name__ == "__main__":
    result = []
    req = input()
    sub_req_or = req.split('|', 'ИЛИ')
    for sub_or in sub_req_or:
        sub_or = sub_or.strip()
        if '&' in sub_or or 'И' in sub_or:
            sub_req_and = sub_or.split('&', 'И')
            intersect = set([])
            for idx, sub_and in enumerate(sub_req_and):
                docs = find_docs_contains(word=sub_and)
                if idx == 0:
                    intersect |= docs
                else:
                    intersect = set.intersection(intersect, docs)
            docs = list(intersect)
        else:
            docs = find_docs_contains(word=sub_or)
        result += docs
    print(result)
