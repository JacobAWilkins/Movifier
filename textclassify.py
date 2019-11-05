#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 17:32:00 2019

@author: jacobwilkins
"""
'''
import sklearn
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split

from sklearn import metrics
'''
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.stem import PorterStemmer
import re

class Textclassify(object):
    
    genres = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentory",
              "Drama", "Family", "Fantasy", "Foreign", "History", "Horror", "Music",
              "Mystery", "Science Fiction", "Thriller", "TV Movie", "War", "Western"]
    
    stopwords = set([
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by',
        'for', 'if', 'in', 'into', 'is', 'it',
        'no', 'not', 'of', 'on', 'or', 's', 'such',
        't', 'that', 'the', 'their', 'then', 'there', 'these',
        'they', 'this', 'to', 'was', 'will', 'with'
    ])
    
    punctuation = re.compile('[~`!@#$%^&*()+={\[}\]|\\:;"\',<.>/?]')
    
    def __init__(self, trainData):
        self.trainData = trainData
    
    def cleanDescr(self, descr):
        descr = self.punctuation.sub(' ', descr)
        ps = PorterStemmer()
        
        for token in descr.split():
            
            token = token.lower().strip() #strip whitespace
            token = ps.stem(token) #stem the token

            if token in self.stopwords:
                descr = self.token.sub(' ', descr)
        return descr
    
    def createFeatVect(self, trainData, genre):
        descriptions = []
        for movie in trainData.items():
            if (movie.get['genre'] == genre): descriptions.append(self.cleanDescr(movie.get['text']))
        vectorizer = CountVectorizer(min_df = 0, lowercase = True)
        vectorizer.fit(descriptions)
        vectorizer.transform(descriptions).toarray()
        return descriptions
    
    def classify(self, query):
        results = []
        
        query = self.cleanDescr(query)
        vectorizer = CountVectorizer(min_df = 0, lowercase = True)
        vectorizer.fit(query)
        vectorizer.transform(query).toarray()
        
        for genre in self.genres:
            classifier = LogisticRegression()
            featVect = self.createFeatVect(self.trainData, genre)
               
        return
