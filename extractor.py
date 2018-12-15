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

    filtered_tokens = list(filter(lambda t: t[1] not in filter_tags, tagged_tokens))

    filtered_tokens = list(map(lambda t: t[0], filtered_tokens))

    return " ".join(filtered_tokens)


def keep_content(content, keep_tags):
    tokens = word_tokenize(content)
    tagged_tokens = nltk.pos_tag(tokens)

    filtered_tokens = list(filter(lambda t: t[1] in keep_tags, tagged_tokens))

    filtered_tokens = list(map(lambda t: t[0], filtered_tokens))

    return filtered_tokens


def extractType(content):
    filter_tags = ["DT", "JJ", "JJS", "JJR", "JJ"]

    filtered_content = filter_content(content, filter_tags)

    matches = re.search(r'(is|was|are|were|be|mean|means) (.+)', filtered_content)

    typ = None
    if matches:
        keep_tags = ["NN", "NNS", "NNP", "NNPS"]
        matched_content = matches.group(2)
        typs = keep_content(matched_content, keep_tags)
        if len(typs) > 0:
            typ = typs[0]

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
            typ = extractType(page.content)
            print(typ)
            if typ:
                output.write(page.title + "\t" + typ + "\n")
