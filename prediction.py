
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
import pickle


# In[41]:


MultinomialNB_model = pickle.load(open("Multinomial Naive Bayes.pkl", "rb"))


# In[42]:


BernoulliNB_model = pickle.load(open("Bernoulli Naive Bayes.pkl", "rb"))


# In[43]:


cv = pickle.load(open("vectorizer.pickle", 'rb'))


# ### Cleaning

# In[44]:


en_stopwords = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')
ps = PorterStemmer()


# In[45]:


def getCleanReview(review):
    review = review.lower()
    review = review.replace('<br /><br />', ' ')

    # Tokenize
    tokens = tokenizer.tokenize(review)
    new_tokens = [token for token in tokens if token not in en_stopwords]
    stemmed_tokens = [ps.stem(token) for token in new_tokens]

    cleaned_review = ' '.join(stemmed_tokens)

    return cleaned_review


# In[52]:


def prediction(review):
    rev1 = getCleanReview(review)
    rev1 = [rev1]
    x_test_vec = cv.transform(rev1)
    pred = MultinomialNB_model.predict(x_test_vec)
    return pred
