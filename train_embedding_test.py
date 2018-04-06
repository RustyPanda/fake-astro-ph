import pytest

import mongomock

import train_embedding


@pytest.fixture
def mock_paper_data():
    return [
        {
            'title': ['galaxies are cool and clusters are not'],
            'abstract': 'first_abstract'
        },

        {
            'title': ['clusters are much cooler than galaxies'],
            'abstract': 'second_abstract'
        },
    ]


@pytest.fixture
def papers(mock_paper_data):
    papers = mongomock.MongoClient().db.collection
    papers.insert_many(mock_paper_data)
    return papers


@pytest.fixture
def corpus(papers):
    return train_embedding.Corpus(papers)


def test_iter(corpus):
    print([title for title in corpus])
    # TODO use asserts


def test_get_vectors():
    model = train_embedding.get_vectors(['galaxies and clusters'.split(), 'cluster and galaxies'.split()])
    model.similarity('galaxies', 'clusters')


def test_get_vectors_from_corpus(corpus):
    model = train_embedding.get_vectors(corpus)
    print(model.similarity('galaxies', 'clusters'))
