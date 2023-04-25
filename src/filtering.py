from typing import List
import nltk
import re
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import time

nltk.download('stopwords')
nltk.download('wordnet')


def preprocess_docs(docs: dict):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    # preprocess text
    processed_docs = {}
    for doc_id, doc in docs.items():
        tokens = nltk.tokenize(doc)
        tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum() and token.lower() not in stop_words]
        processed_docs[doc_id] = tokens
    
    return processed_docs


def train_lda(docs: dict):

    # create dictionary of tokens in corpus
    corpus_dict = corpora.Dictionary(docs.values())
    # create bag-of-words corpus
    bow_corpus = {doc_id: corpus_dict.doc2bow(docs) for doc_id, doc in docs.items()}

    # start LDA training timer
    start_time = time.time()
    print(f'LDA model training started at {start_time}')
    # train LDA model
    lda_model = models.LdaModel(list(bow_corpus.values()), num_topics=10, id2word=corpus_dict, passes=20)
    # end LDA training timer
    end_time = time.time()
    print(f'LDA model training finished at {end_time}')
    print(f'Training the LDA model time took {end_time - start_time} seconds')

    asthma_related_docs = []

    for doc_id, doc_bow in bow_corpus.items():
        doc_topics = lda_model.get_document_topics(doc_bow, minimum_probability=0.2)
        for topic_id, topic_prob in doc_topics:
            # get the top 10 words for the current topic
            topic_top_words = lda_model.show_topic(topic_id, topn=10)
            top_words = [word for word, prob in topic_top_words]
            
            # check if "asthma" is among the top words in the topic
            if "asthma" in top_words:
                asthma_related_docs.append((doc_id, docs[doc_id]))
    
    return asthma_related_docs
    

def filter_relevant_docs(cleaned_docs: dict, keywords: List[str]) -> dict:

    # preprocess tokens in doc
    cleaned_docs = preprocess_docs(cleaned_docs)

    # train model
    asthma_docs = train_lda(cleaned_docs)

    return asthma_docs