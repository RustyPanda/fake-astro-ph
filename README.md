# fake-astro-ph

We’d like to
1. Save thousands of arXiv titles via the ADS API (probably into mongoDB to avoid re-querying when we want to search/filter later) https://github.com/andycasey/ads
2. Save the titles into a text files
3. Generate a word embedding with Gensim: https://radimrehurek.com/gensim/
4. Given an embedding, generate a grammar with https://spacy.io/
5. Given word embedding and grammar, make random titles with https://github.com/jsvine/markovify
6. If time allows, make a website to share!

It’s a bit like http://davidsd.org/2010/03/the-snarxiv/ but with an NLP approach rather than a large set of rules


Notes:

We should be able to read in our abstracts by directly querying the database: see https://radimrehurek.com/gensim/tut1.html#corpus-streaming-one-document-at-a-time