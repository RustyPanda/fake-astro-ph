
# see http://ads.readthedocs.io/en/latest/
# example search: arxiv_class:"Astrophysics of Galaxies"

import ads
# don't put this on github


api_token = 'HBX51eAinpW4XVvNwXkfuvrpzRwvKEUt7zS6NPsc'
ads.config.token = api_token

useful_attributes = [
    'abstract',
    'author',
    'aff',
    'bibcode',
    'citation_count',
    'database',
    'doctype',
    'keyword',
    'page',
    'property',
    'pub',
    'pubdate',
    'read_count',
    'title',
    'year'
]

query_text = 'arxiv_class:"Astrophysics of Galaxies"'
q = ads.SearchQuery(q=query_text, fl=useful_attributes, rows=20)  # max allowed rows
n = 0
# wipe files beforehand
titles = open("titles.txt", "w")
abstracts = open("abstracts.txt", "w")
titles_and_abstracts = open("titles_and_abstracts.txt", "w")
for paper in q:
    print(paper.title)
    titles.write(paper.title[0] + '\n\n')
    abstracts.write(paper.abstract + '\n\n')
    titles_and_abstracts.write(paper.title[0] + '\n' + paper.abstract + '\n\n')
    # print(paper.citation_count)
    # print(paper.abstract)
    # print(paper.pubdate)
    # print(paper.pub)
    # print(paper.read_count)
    # print(paper.database)
    # print(paper.year)
    n += 1
    print(n)
    # if n > 80:
#     break
print(q.response.get_ratelimits())
