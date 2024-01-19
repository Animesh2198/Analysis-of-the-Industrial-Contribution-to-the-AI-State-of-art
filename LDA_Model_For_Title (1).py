#import important libraries  

import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

nltk.download('stopwords')
nltk.download('wordnet')

# The below lines will pre-process on the abstract column and extract individual terms. 

titles = df['Title'].values.tolist()

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

tokenizer = RegexpTokenizer(r'\w+')
titles = [tokenizer.tokenize(title.lower()) for title in titles]
stop_words = set(stopwords.words('english'))
titles = [
    [lemmatizer.lemmatize(word) for word in title if word not in stop_words] 
    for title in titles
]
titles = [
    [stemmer.stem(word) for word in title] 
    for title in titles
]

min_word_length = 3
titles = [[word for word in title if len(word) >= min_word_length] for title in titles]


# Here we will create a dictionary and corpus for topic modeling. 
dictionary = corpora.Dictionary(titles)
corpus = [dictionary.doc2bow(title) for title in titles]

# We will train an LDA model with specified parameters.
num_topics = 10
lda_model = models.LdaModel(corpus=corpus[:-1],
                            id2word=dictionary,
                            num_topics=num_topics,
                            random_state=100,
                            update_every=1,
                            chunksize=100,
                            passes=10,
                            alpha="auto")

# Print the topics discovered.

for topic_num in range(num_topics):
    print(f"Topic {topic_num + 1}: {lda_model.print_topic(topic_num)}")
