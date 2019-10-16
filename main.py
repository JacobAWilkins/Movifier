#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 13:26:44 2019

@author: jacobwilkins
"""

from flask import Flask, render_template, flash
from forms import TextSearchForm
from markupsafe import Markup
import csv, movieclassifier, shutil, time, re

# holds the movie results from the TextSearchForm
movies = []

# initial movie classifier
data_dir = '/home/JacobWilkins/Movifier/tmp/movie_index'
shutil.rmtree(data_dir, ignore_errors=True)
mc = movieclassifier.Movieclassifier(data_dir)

# index all movies at start
with open('/home/JacobWilkins/Movifier/movies_metadata.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    doc_times = []
    counter = 0 #used for testing
    # index each movie by title and description
    for row in reader:
        doc_id = row['original_title']
        body = row['overview']
        
        time_start = time.time()
        mc.index(doc_id, {'text': body})
        time_end = time.time() - time_start
        doc_times.append(time_end)
        counter += 1 #test
        if counter > 1000: #only index first 1000 rows
            break
    # average time to index a movie
    doc_time_avg = sum(doc_times) / len(doc_times)
        

# search query submitted from TextSearchForm
def query(descr, numRes):
    start = time.time()
    results, terms = mc.search(descr, 0, numRes)
    searchTime = time.time() - start
    hits = results.get('total_hits', 0)
    movieData = results.get('results')
    
    termsOrig = mc.get_tokens(descr)
    regStr = ""
    for term in termsOrig:
        s1 = "(\\b" + str(term) + "\\b)|"
        regStr += s1
    regStr = regStr[:-1]
    print(regStr)
    regex = re.compile(r"%s" % regStr, re.I)
    # makes sure movies doesn't have data from previous search
    if bool(movies):
        movies.clear()
    # highlight the terms in the movie descriptions  
    #temp1 = ""; temp2 = ""
    d2 = {}
    for res in movieData:
        text = res.get('text')
        i = 0; output = ""; temp1 = ""; temp2 = ""
        for m in regex.finditer(text):
            output += "".join([text[i:m.start()], "<strong><span style='background-color:#FFFF00'>", text[m.start():m.end()], "</span></strong>"])
            i = m.end()
            temp1 = output
            temp2 = text[m.end():]
        s2 = "".join([temp1, temp2])
        d1 = {'text': Markup(u"%s" % s2)}
        if not s2 == "":
            if not d1 == d2:
                res.update(d1)
                d2 = d1
        # add each result to movies dict
        movies.append(res)
    return hits, searchTime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'D22B5C72F638152BB566B67B3CF76'

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = TextSearchForm()
    if form.validate_on_submit():
        descr = form.movieDescription.data
        numRes = form.numResults.data
        total_hits, searchTime = query(descr, numRes)
        flash(Markup(f'Query successfully submitted! Found <b>%s</b> results in <b>%0.3f</b> seconds!' % (total_hits, searchTime)), 'success')
    return render_template("home.html", form=form, movies=movies)

#if __name__ == "__main__":
#    app.run(debug = False)
