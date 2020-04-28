import numpy as np
import pandas as pd
import os
import nltk
import re, string, unicodedata
import seaborn as sns
import sys
import os
import gensim
import sklearn
from bs4 import BeautifulSoup
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from gensim.models import word2vec, Word2Vec
from pandas import Series
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, BayesianRidge
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn import ensemble


def predict(text):
    model_lr = joblib.load('static/save/model_lr_1000k.pkl')
    model_svm = joblib.load('static/save/model_svm.pkl')
    model_random_forest_regressor = joblib.load('static/save/model_random_forest.pkl')
    model_bayes_ridge = joblib.load('static/save/model_bayes_1000k.pkl')
    data = {'comment': Series([text])}
    data = pd.DataFrame(data)
    print(data)
    data['comment'] = data['comment'].apply(remove_between_square_brackets)
    data['comment'] = data['comment'].apply(remove_special_characters)
    data['comment'] = data['comment'].apply(simple_stemmer)
    data['comment'] = data['comment'].apply(remove_stopwords)

    data['comment'] = data.comment.str.lower()
    data['document_sentences'] = data.comment.str.split('.')
    data['tokenized_sentences'] = data['document_sentences']
    data['tokenized_sentences'] = list(
        map(lambda sentences: list(map(nltk.word_tokenize, sentences)), data.document_sentences))
    data['tokenized_sentences'] = list(
        map(lambda sentences: list(filter(lambda lst: lst, sentences)), data.tokenized_sentences))
    print(data)
    # sentence = data['tokenized_sentences'][0]
    W2Vmodel = gensim.models.word2vec.Word2Vec.load("static/Word2Vec.w2v").wv

    data['sentence_vectors'] = list(map(lambda sen_group:
                                        sentence_vectors(W2Vmodel, sen_group),
                                        data.tokenized_sentences))
    text = vectors_to_feats(data, 300)

    lr_y_predict = model_lr.predict(text)
    svm_y_predict = model_svm.predict(text)
    bayes_y_predict = model_bayes_ridge.predict(text)
    random_forest_y_predict = model_random_forest_regressor.predict(text)

    return lr_y_predict, svm_y_predict, random_forest_y_predict, bayes_y_predict


def sentence_vectors(model, sentence):
    # Collecting all words in the text
    #     print(sentence)
    words = np.concatenate(sentence)
    # words = sentence
    # print(sentence)
    # Collecting words that are known to the model
    model_voc = set(model.vocab.keys())
    # print(model_voc)
    sent_vector = np.zeros(model.vector_size, dtype="float32")

    # Use a counter variable for number of words in a text
    nwords = 0
    # Sum up all words vectors that are know to the model
    for word in words:
        # print(word)
        if word in model_voc:
            sent_vector += model[word]
            nwords += 1.

    # Now get the average
    if nwords > 0:
        sent_vector /= nwords
    return sent_vector


def vectors_to_feats(df, ndim):
    index = []
    for i in range(ndim):
        df[f'w2v_{i}'] = df['sentence_vectors'].apply(lambda x: x[i])
        index.append(f'w2v_{i}')
    return df[index]


def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


# Removing the square brackets
def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)


# Removing the noisy text
def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text


# Apply function on review column

def remove_special_characters(text, remove_digits=True):
    pattern = r'[^a-zA-z0-9\s]'
    text = re.sub(pattern, '', text)
    return text


# Apply function on review column
def simple_stemmer(text):
    ps = nltk.porter.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text


# Apply function on review column


# Tokenization of text
tokenizer = ToktokTokenizer()
# Setting English stopwords
stopword_list = nltk.corpus.stopwords.words('english')
stop = set(stopwords.words('english'))
print(stop)


# removing the stopwords

def remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text
# Apply function on review column


#
# if __name__ == '__main__':
#     print(predict("This is a great game.  I've even got a number of non game players enjoying it.  Fast to learn and always changing."))
#     # text = "you are super good"
#     # sentence = map(nltk.word_tokenize, text)
#     # sentence = filter(lambda lst: lst, sentence)
#     # print(sentence)
#     # print(sklearn.__version__ )
