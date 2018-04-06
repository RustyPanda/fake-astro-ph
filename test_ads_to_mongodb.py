import pytest

import mongomock

import ads_to_mongodb

@pytest.fixture
def query_params():
    return {
        'q': 'star',
        'fl': ['title', 'abstract'],
        'rows': 3
    }


@pytest.fixture
def q():
    return 'star'


# @pytest.fixture
# def db():
#     return mongomock.MongoClient().db


@pytest.fixture
def collection():
    return mongomock.MongoClient().db.collection


def mock_ads_query(q, fl=None, rows=None):

    if fl is None:
        fl = ['title', 'abstract']

    first_response = dict(zip(
        fl,
        map(lambda x: 'first_' + x, fl)
    ))
    second_response = dict(zip(
        fl,
        map(lambda x: 'second_' + x, fl)
    ))

    if rows == 1:
        return [first_response]
    else:
        return [first_response] + [second_response]


def test_save_query_to_db(query_params, collection):
    ads_to_mongodb.save_query_to_collection(query_params, collection)
    # check updated db has new data
    print(collection.find_one())


def test_save_ads_to_db(collection):  # will construct appropriate query inside
    ads_to_mongodb.save_ads_to_collection(collection, query_max_rows=2)
    # check updated db has new data
    print(collection.find_one())
