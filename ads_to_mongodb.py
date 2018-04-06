import ads

def save_ads_to_collection(collection):

    useful_attributes = [
        'abstract',
        'author',
        'aff',
        'bibcode',
        'bibtex',
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
    query_params = dict(q=query_text, fl=useful_attributes, rows=5)  #  max allowed rows
    save_query_to_collection(query_params, collection)


def save_query_to_collection(query_params, collection, api_token=None):

    if api_token is None:
        with open('api_token.txt', 'r') as f:
            api_token = f.read()
    # don't put this on github
    api_token =
    ads.config.token = api_token

    q = ads.SearchQuery(**query_params)  #  max allowed rows
    all_responses = []
    for paper in q:
        response = {}
        for field in query_params['fl']:
            response[field] = getattr(paper, field)
        all_responses.append(response)

    # titles.write(paper.title[0] + '\n\n')
    # abstracts.write(paper.abstract + '\n\n')
    # titles_and_abstracts.write(paper.title[0] + '\n' + paper.abstract + '\n\n')
    # print(paper.citation_count)
    # print(paper.abstract)
    # print(paper.pubdate)
    # print(paper.pub)
    # print(paper.read_count)
    # print(paper.database)
    # print(paper.year)

    collection.insert_many(all_responses)  # modifies inplace
