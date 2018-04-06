import spacy

nlp = spacy.load('en_core_web_lg')
tokens = nlp(u'dog cat banana sasquatch')

for token in tokens:
    print(token.text, token.has_vector, token.vector_norm, token.is_oov)
for token1 in tokens:
    for token2 in tokens:
        print(token1.similarity(token2))