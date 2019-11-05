#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 13:26:44 2019

@author: jacobwilkins
"""

from flask import Flask, render_template, flash, url_for
from forms import TextSearchForm, TextClassifyForm
from markupsafe import Markup
import csv, textsearch, textclassify, shutil, time, re
from ast import literal_eval

# holds the movie results from the TextSearchForm
movies = []
trainData = []
classifyRes = {
    "Action": "0 %",
    "Adventure": "0 %",
    "Animation": "0 %",
    "Comedy": "0 %",
    "Crime": "0 %",
    "Documentory": "0 %",
    "Drama": "0 %",
    "Family": "0 %",
    "Fantasy": "0 %",
    "Foreign": "0 %",
    "History": "0 %",
    "Horror": "0 %",
    "Music": "0 %",
    "Mystery": "0 %",
    "Science Fiction": "0 %",
    "Thriller": "0 %",
    "TV Movie": "0 %",
    "War": "0 %",
    "Western": "0 %",
}

shutil.rmtree('/temp/movie_index', ignore_errors=True) # remove directory before indexing restarts
ts = textsearch.Textsearch('/temp/movie_index') # initialize text search

# index all movies at start
with open('movies_metadata.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    doc_times = []
    counter = 0 #used for testing
    # index each movie by title and description
    for row in reader:
        doc_id = row['original_title']
        body = row['overview']
        link = row['imdbId']
        genres = row['genres']
        poster = row['poster_path']
        
        ts.index(doc_id, {'text': body}, {'link': link}, {'poster': poster})
        
        trainData.append({
            'text': body,
            'genres': literal_eval(genres),
        })
        counter += 1 #test
        if counter > 100: break #only index first 100 rows
        
#tc = textclassify.Textclassify(trainData) # initialize text classify

# search query submitted from TextSearchForm
def textSearchQuery(descr, numRes):
    start = time.time()
    results, terms = ts.search(descr, 0, numRes)
    searchTime = time.time() - start
    hits = results.get('total_hits', 0)
    movieData = results.get('results')
    
    terms = ts.parse_query(descr)
    terms = sorted(terms, key = len, reverse=True)
    regStr = ""
    for term in terms:
        s1 = "(" + str(term) + ")|"
        regStr += s1
    regex = re.compile(r"%s" % regStr[:-1], re.I)
    # makes sure movies doesn't have data from previous search
    if bool(movies): movies.clear()
    # highlight the terms in the movie descriptions
    d2 = {}
    for res in movieData:
        text = res[1].get('text')
        i = 0; output = ""; temp1 = ""; temp2 = ""
        print(text)
        for m in regex.finditer(text):
            output += "".join([text[i:m.start()], "<strong><span style='background-color:#FFFF00'>", text[m.start():text.find(' ', m.end())], "</span></strong>"])
            i = text.find(' ', m.end())
            temp1 = output
            temp2 = text[text.find(' ', m.end()):]
        s2 = "".join([temp1, temp2])
        d1 = {'text': Markup(u"%s" % s2)}
        if not s2 == "":
            if not d1 == d2:
                res[1].update(d1)
                d2 = d1
        # alter links depending on length
        if len(res[0].get('link')) == 6:
            res[0].update({'link': "0" + res[0].get('link')})
        if len(res[0].get('link')) == 5:
            res[0].update({'link': "00" + res[0].get('link')})
        # add each result to movies dict
        movies.append(res)
    return hits, searchTime

def textClassify(descr):
    start = time.time()
    searchTime = time.time() - start
    return searchTime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'D22B5C72F638152BB566B67B3CF76'

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = TextSearchForm()
    if form.validate_on_submit():
        descr = form.movieDescription.data
        numRes = form.numResults.data
        total_hits, searchTime = textSearchQuery(descr, numRes)
        flash(Markup(f'Query successfully submitted! Found <b>%s</b> results in <b>%0.3f</b> seconds!' % (total_hits, searchTime)), 'success')
    return render_template("home.html", form=form, movies=movies)

@app.route("/classify", methods=['GET', 'POST'])
def classify():
    form = TextClassifyForm()
    if form.validate_on_submit():
        descr = form.movieDescription.data
        searchTime = textClassify(descr)
        flash(Markup(f'Query successfully submitted! Found results in <b>%0.3f</b> seconds!' % searchTime), 'success')
    return render_template("classify.html", form=form, classifyRes=classifyRes)

if __name__ == "__main__":
    app.run(debug = True)
