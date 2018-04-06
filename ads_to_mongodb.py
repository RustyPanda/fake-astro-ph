import datetime

import ads


def save_ads_to_collection(collection, query_max_rows=2000):

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

    # we want to query every two months or so to avoid the 2k row limit
    # TODO refactor out to main.py?
    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2018, 4, 1)
    interval = datetime.timedelta(days=15)

    query_start_date = start_date
    query_end_date = start_date + interval
    while query_end_date < end_date:
        # date expects format 2000-01-01 YYYY-MM-DD
        # query_text = 'arxiv_class:"Astrophysics of Galaxies" pubdate:[{} TO {}]'.format(
        query_text = 'arxiv_class:("High Energy Astrophysical Phenomena" OR "Instrumentation and Methods for Astrophysics" OR "Solar and Stellar Astrophysics" OR "Earth and Planetary Astrophysics" OR "Cosmology and Nongalactic Astrophysics" OR "Astrophysics of Galaxies") AND pubdate:[{} TO {}]'.format(
            query_start_date, query_end_date)
        query_params = dict(q=query_text, fl=useful_attributes, rows=query_max_rows)  #  max allowed rows
        print('Making query {}'.format(query_text))  # temp
        save_query_to_collection(query_params, collection)
        query_start_date += interval
        query_end_date += interval


def save_query_to_collection(query_params, collection, api_token=None):

    if api_token is None:
        # don't put this on github
        with open('api_token.txt', 'r') as f:
            ads.config.token = f.read()

    q = ads.SearchQuery(**query_params)  #  max allowed rows
    all_responses = []
    for paper in q:
        response = {}
        for field in query_params['fl']:
            response[field] = getattr(paper, field)
        all_responses.append(response)

    if len(all_responses) > 0:
        print('Inserting {} papers'.format(len(all_responses)))
        collection.insert_many(all_responses)  # modifies inplace
