# Import statement for data analysis and NLP
import nltk
import pandas as pd
import numpy as np
import string
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier

useless_words = nltk.corpus.stopwords.words("english") + list(string.punctuation)

def build_bag_of_words_features_filtered(words):
    return {
        word:1 for word in words \
        if not word in useless_words}

df = pd.read_excel('data/dataset.xlsx')
df = df.dropna()
positive_data = []
negative_data = []
neutral_data = []
for i in range(0, len(df)):
    row = df.iloc[i]
    if(row["sentiment"] == 'positive'):
        positive_data.append(({row["word"]:1}, 'pos'))
    elif(row["sentiment"] == 'negative'):
        negative_data.append(({row["word"]:1}, 'neg'))
    elif(row["sentiment"] == 'neutral'):
        neutral_data.append(({row["word"]:1}, 'neu'))

new_classifier = NaiveBayesClassifier.train((positive_data + negative_data + neutral_data))

def getEmotion(message):
    message = message.lower()
    temp = message.split()
    words = []
    flag = 0
    for i in range(0, len(temp)):
        if(flag == 1):
            flag = 0 
            continue
        print(temp[i])
        if(temp[i] == 'not'):
            if(i+1 != len(temp)):
                t = ("%s %s")%(temp[i], temp[i+1])
                words.append(t)
                flag = 1
        else:
            words.append(temp[i])
    build_bag_of_words_features_filtered(words)
    return new_classifier.classify(build_bag_of_words_features_filtered(words))

