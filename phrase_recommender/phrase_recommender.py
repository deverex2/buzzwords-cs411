from __future__ import unicode_literals 
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import nltk
nltk.download('stopwords')

import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
# If there are issues in installing gensim, refer to:
# https://stackoverflow.com/questions/22738077/backports-lzma-lzmamodule-c11518-fatal-error-lzma-h-no-such-file-or-direct


# spacy for lemmatization
import spacy

# NLTK Stop words
from nltk.corpus import stopwords

# genres,lyrics,artist,url,release_date,title,billboard_rank,artist_id,id

# ref: https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/

def sanitize_song(song):
    #remove single quotes
    song = song.replace("'", "")
    song = song.replace("(", "")
    song = song.replace(")", "")
    song = song.replace("!", "")
    song = song.replace("?", "")
    return song

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    stop_words = stopwords.words('english')
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en
    nlp = spacy.load('en', disable=['parser', 'ner'])
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def get_topics(text, num_topics, min_count, threshold):
    stop_words = stopwords.words('english')

    text = sanitize_song(text)
    sentences = text.split('\t')
    data_words = list(sent_to_words(sentences))
    # print data_words

    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=min_count, threshold=threshold) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=threshold)  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops, bigram_mod)

    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en
    nlp = spacy.load('en', disable=['parser', 'ner'])

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams)
    # data_lemmatized = data_words_bigrams
    

    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                               id2word=id2word,
                                               num_topics=num_topics, 
                                               random_state=100,
                                               update_every=1,
                                               per_word_topics=True)

    # pprint(lda_model.print_topics())

    return get_topics_from_model(lda_model.show_topics())
    # doc_lda = lda_model[corpus]

    # # Compute Perplexity
    # print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

    # # Compute Coherence Score
    # coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
    # coherence_lda = coherence_model_lda.get_coherence()
    # print('\nCoherence Score: ', coherence_lda)


def get_topics_gram(text, num_topics, min_count, threshold, gram):
    text = get_gram_text(text,gram)
    
    stop_words = stopwords.words('english')

    text = sanitize_song(text)
    sentences = text.split('\t')
    data_words = list(sent_to_words(sentences))

    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)

    nlp = spacy.load('en', disable=['parser', 'ner'])

    data_lemmatized = lemmatization(data_words_nostops)

    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_lemmatized

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                               id2word=id2word,
                                               num_topics=num_topics, 
                                               random_state=100,
                                               update_every=1,
                                               per_word_topics=True)

    # pprint(lda_model.print_topics())

    return get_topics_from_model(lda_model.show_topics())

def get_topics_from_model(topic_dist):
    topics=set()
    for _, td in topic_dist:
        for tops in td.split("+"):
            top = tops.split("*")[1][1:-1]
            topics.add(top)
    return list(topics)


def get_gram_text(data, gram):
    text = data.split()
    ret=[]
    for i in xrange(0,len(text)-gram):
        chunk = text[i:i+gram]
        ret.append('_'.join(chunk))
    return ' '.join(ret)


if __name__ == '__main__':
    import pandas as pd
    from collections import defaultdict

    data = pd.read_csv('./data.csv', usecols=['genre', 'lyrics', 'release_date'])

    # song_dict[genre][year] will return all lyrics for that genre in that year
    song_dict = defaultdict(lambda: defaultdict(str))

    for _, row in data.iterrows():
        year = row['release_date'].split('-')[0]
        song_dict[row['genre']][year] += "    "+row['lyrics'].encode('utf-8')

    # get_topics(song_dict['Pop']['2005'],3,10)

    txt = song_dict['Pop']['2006']

    print get_topics(txt,3,10,20)
    print "---------------"
    print get_topics_gram(txt,3,3,5,3)