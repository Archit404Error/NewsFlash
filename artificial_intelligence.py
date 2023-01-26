import pickle
import re

import nltk
import numpy as np
import tensorflow as tf
from gensim.models import Doc2Vec
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tensorflow.keras.models import load_model

vec_model = Doc2Vec.load("./ai_models/Doc2Vec/article_bias_doc2vec.model")
article_nn = load_model("./ai_models/article_bias_nn.h5")
engl_stops = set(stopwords.words("english"))


def clean(text):
    text = re.sub(r"\|\|\|", r" ", text)
    text = text.replace("„", "")
    text = text.replace("“", "")
    text = text.replace('"', "")
    text = text.replace("'", "")
    text = text.replace("-", "")
    text = text.lower()
    return text


def remove_stopwords(text):
    return " ".join([word for word in text.split() if word not in engl_stops])


def tokenize(text):
    return list(filter(lambda word: len(word) > 3, word_tokenize(text)))


def preprocess(text):
    return vec_model.infer_vector(tokenize(remove_stopwords(clean(text))))


def predict_bias(article_text):
    print(article_text)
    art_vec = np.asarray(preprocess(article_text))
    art_vec = art_vec.reshape(1, 500)
    labels = ["republican", "democratic"]
    pred = article_nn.predict(art_vec)
    return labels[np.argmax(pred)], float(np.max(pred))


def process_batch(contents):
    for i, content in enumerate(contents):
        contents[i] = predict_bias(content) if content else ("", 0.0)
