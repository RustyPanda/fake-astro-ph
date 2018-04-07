import pytest

import mongomock

from embedder import train_embedding


@pytest.fixture
def mock_paper_data():
    return [
        {
            'title': ['galaxies are cool and clusters are not'],
            'abstract': 'first_abstract',
            'author': ['author_a'],
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


def test_corpus_fields(corpus):
    print(list(corpus.abstracts))
    print(list(corpus.titles))
    print(list(corpus.pubdate))
    print(list(corpus.aff))
    print(list(corpus.author))


def test_get_vectors():
    model = train_embedding.embed_corpus(['galaxies and clusters'.split(), 'cluster and galaxies'.split()])
    model.similarity('galaxies', 'clusters')


def test_get_vectors_from_corpus(corpus):
    model = train_embedding.embed_corpus(corpus)
    print(model.similarity('galaxies', 'clusters'))
