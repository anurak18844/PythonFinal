import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from io import StringIO
from pythainlp.corpus.common import thai_stopwords
from pythainlp import word_tokenize

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

import pickle


df = pd.read_csv('data_trainmodel.csv', sep=',', names=['TEXT', 'TOPIC'], header=None)

col=['TEXT','TOPIC']
df = df[col]
df = df[pd.notnull(df['TEXT'])]

df.columns = ['TEXT', 'TOPIC']

df['TOPIC_ID']=df['TOPIC'].factorize()[0]
topic_id_df = df[['TOPIC', 'TOPIC_ID']].drop_duplicates().sort_values('TOPIC_ID')
topic_to_id = dict(topic_id_df.values)
id_to_topic = dict(topic_id_df[['TOPIC_ID','TOPIC']].values)

thai_stopwords = list(thai_stopwords())
thai_stopwords.append('อ่ะ')
thai_stopwords.append('อะ')

def text_process(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":", "!", '"', "ๆ", "ฯ", "#", ",", "-", "/", "=", "(", ")" ,"+","|"))
    final = word_tokenize(final)
    final = " ".join(word for word in final)
    final = " ".join(word for word in final.split() if word not in ('อะ','อ่ะ'))
    final = " ".join(word for word in final.split() if word.lower not in thai_stopwords)
    return final

df['TEXT TOKENS'] = df['TEXT'].apply(text_process)

X = df[['TEXT TOKENS']]
y = df['TOPIC_ID']

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=101)

cvec = CountVectorizer(analyzer=lambda x:x.split(' '))
cvec.fit_transform(X_train['TEXT TOKENS'])

train_bow = cvec.transform(X_train['TEXT TOKENS'])

pd.DataFrame(train_bow.toarray(), columns=cvec.get_feature_names(), index=X_train['TEXT TOKENS'])

clf = RandomForestClassifier()
clf.fit(train_bow, y_train)

pickle.dump(clf, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl','rb'))

def create_mybow(my_texts):
    my_tokens = [text_process(t) for t in my_texts]
    my_bow = cvec.transform(pd.Series(my_tokens))
    return my_bow



