'''Extracts type facts from a wikipedia file
usage: extractor.py wikipedia.txt output.txt

Every line of output.txt contains a fact of the form
    <title> TAB <type>
where <title> is the title of the Wikipedia page, and
<type> is a simple noun (excluding abstract types like
sort, kind, part, form, type, number, ...).

If you do not know the type of an entity, skip the article.
(Public skeleton code)'''

from parser import Parser
import sys
import re
import nltk
from nltk.tokenize import word_tokenize

if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(-1)


def filter_content(content, filter_tags):
    tokens = word_tokenize(content)
    tagged_tokens = nltk.pos_tag(tokens)

    filtered_tokens = []

    for i in range(len(tagged_tokens)):
        t = tagged_tokens[i]

        if i + 1 != len(tagged_tokens):
            next_t = tagged_tokens[i + 1]
            if t[1] not in filter_tags and next_t[0] != "'s":
                filtered_tokens.append(t[0])

        if t[0] == "'s" and tagged_tokens[i + 1][1] not in ["RBS"]:
            filtered_tokens.append(tagged_tokens[i + 1][0])

    return " ".join(filtered_tokens)


dic = {
    'NNP': ['NNP', 'NNPS'],
    'NNPS': ['NNP', 'NNPS'],
    'NN': ['NN', 'NNS'],
    'NNS': ['NN', 'NNS']
}


def keep_content(content, keep_tags):
    tokens = word_tokenize(content)
    tagged_tokens = nltk.pos_tag(tokens)

    filtered_tokens = []
    l = len(tagged_tokens)
    for i in range(l):
        t = tagged_tokens[i]
        if t[1] in keep_tags:
            if i != l - 1:
                next_t = tagged_tokens[i + 1]
                if next_t[1] not in dic[t[1]]:
                    filtered_tokens.append(t[0])
            else:
                filtered_tokens.append(t[0])

        if t[0] == "'s" and tagged_tokens[i + 1][1] not in ["RBS"]:
            tagged_tokens[i + 1] = (tagged_tokens[i + 1][0], "NN")

    return filtered_tokens


def extractType(content):
    filter_tags = ["DT", "JJ", "JJS", "JJR", "JJ"]
    keep_tags = ["NN", "NNS", "NNP", "NNPS"]

    filtered_content = filter_content(content, filter_tags)

    matches = re.search(r'(is|was|are|were|be|mean|means) (.+)', filtered_content)

    matched_content = filtered_content
    if matches:
        matched_content = matches.group(2)

    matches = re.search(r'(type of|area of|range of|body of|word for|forms of|set of|part of|style of|strip of) (.+)',
                        matched_content)
    if matches:
        old = matched_content
        matched_content = matches.group(2)
        if abs(len(matched_content) - len(old)) > 20:
            matched_content = old

    typs = keep_content(matched_content, keep_tags)

    typ = None
    if typs and len(typs) > 0:
        typ = typs[0]
        # if len(typs) > 1 and typ == "type":
        #     typ = typs[1]

    return typ


with open(sys.argv[2], 'w', encoding="utf-8") as output:
    i = 0
    for page in Parser(sys.argv[1]):
        # print(page.title)
        # print(page.content)
        i += 1
        print(i)
        # if i == 10:
        #     break
        if page.title == "Smash (album)":
            content = page.content.replace(page.title, "")
            typ = extractType(content)
            if typ:
                output.write(page.title + "\t" + typ + "\n")
