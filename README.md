# Movifier
Given **[this](https://www.kaggle.com/rounakbanik/the-movies-dataset)** dataset of movie titles and descriptions from Kaggle, Movifier implements text search using Okapi BM25 to score, classifies movies by genre, and generates captions for movie scenes. The text search takes a description of a movie and outputs a list of similar movies with similar descriptions. Movifier is developed using **[Flask](https://www.fullstackpython.com/flask.html)**, a lightweight WSGI web application framework. The project proposal can be found **[here](https://docs.google.com/document/d/1uDnyLfvAJTHSIp2gLQYVDAONRQX91yI2uVtycHrf1pE/edit?usp=sharing)**.

# Text Search Documentation
* [Deployment Insctructions](#deployment-instructions)
  * [Online](#online)
  * [Localhost](#localhost)
* [Contributions & References](#contributions--references)
* [Data Structures](#data-structures)
  * [Documents Structure](#documents-structure)
  * [Inverted Index Structure](#inverted-index-structure)
* [Algorithms Explained](#algorithms-explained)
  * [Index Algorithm](#index-algorithm)
  * [Search Algorithm (Okapi BM25)](#search-algorithm-okapi-bm25)
* [Optimizations](#optimizations)
  * [Ngrams](#ngrams)
  * [Stop Words](#stop-words)
  * [Punctuation](#punctuation)
  * [Stemming](#stemming)
* [Test Cases](#test-cases)
* [Author](#author)

### Deployment Instructions
##### Online
http://jacobwilkins.pythonanywhere.com/home
##### Localhost
1. Install Flask:
```pip install flask```
2. Run Movifier:
```sudo python main.py```
   Wait for dataset to index movies. This will take a while unless you change the number of movies indexed to a lower number. The default is 1000. You can change this in main.py. Afterwards, you will see a message ``` * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)``` in the terminal.
3. In browser (localhost, port 5000):
```http://127.0.0.1:5000/```

### Contributions & References
* For text search, I used Toastdriven's **[microsearch](https://github.com/toastdriven/microsearch)** repository and added some optimizations. I optimized the text search by adding stemming capabilities using the **[nltk.stem.porter](https://www.nltk.org/_modules/nltk/stem/porter.html)** module. In addition, I added my own Okapi BM25 alogrithm based on the formulas from **[Wikipedia](https://en.wikipedia.org/wiki/Okapi_BM25#The_ranking_function)**
* For the Flask web app API, I used CoreyMschafer's **[Flask_Blog](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog)** repository as a starting point
* I developed an algorithm to highlight the query tokens in the text description results using regular expression. I used **[this](https://www.saltycrane.com/blog/2007/10/using-pythons-finditer-to-highlight/)** post from the Salty Crane blog as a reference

### Data Structures
##### Documents Structure
A field-based dictionary where the keys are field names and the values are the field's contents.
```
{
  "id": "movie-title",
  "text": "This is a movies description",
}
```
##### Inverted Index Structure
A term-based dictionary where the keys are terms and the values are documents/position information.
```
index = {
        'happy': {
            'Toy Story': [3],
        },
        'back': {
            'Terminator': [5, 10],
        },
        ...
    }
```
### Algorithms Explained
##### Index Algorithm
Indexes the first 1000 movies of the movies_metadata.csv dataset. The number of movies indexed can be changed by altering the altering the boundary of the counter. Movies are saved as **[documents](#Documents-Structure)** and the terms are saved into an **[inverted index](#Inverted-Index-Structure)**. The movies are stored in JSON files to allow for easy indexing and searching.
```
with open('/home/JacobWilkins/Movifier/movies_metadata.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    counter = 0
    # index each movie by title and description
    for row in reader:
        doc_id = row['original_title']
        body = row['overview']
        mc.index(doc_id, {'text': body})
        counter += 1
        if counter > 1000: # only index first 1000 rows
            break
```
##### Search Algorithm (Okapi BM25)
For a given document, the **[Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25#The_ranking_function)** ranking score is calculated as
```
score = 0
for term in terms:
    idf = math.log((total_docs - matches[term] + 0.5) / (matches[term] + 0.5))
    score = score + (current_doc.get(term, 0) * idf * (k + 1)) / (current_doc.get(term, 0) + k * (1 - b + (b * (curr_len / avg_len))))
return score
```
where **terms** is the list of terms in the document, **matches** is the first dictionary returned from collect_results(self, terms), **current doc** is the second dictionary returned from collect_results(self, terms), **total_docs** is the total number of documents in the index, **curr_len** is the length of the current document, and **avg_len** is the average length of all the documents. **b** and **k** are used to modify ranking scores to fall in a given range.
### Optimizations
##### Ngrams
Front n-grams of tokens are made from 3 to 6 in gram length.
```
terms = {}
for position, token in enumerate(tokens):
    for window_length in range(min_gram, min(max_gram + 1, len(token) + 1)):
        gram = token[:window_length]
        terms.setdefault(gram, [])
        if not position in terms[gram]:
            terms[gram].append(position)
return terms
```
##### Stop words
Queries are filtered using this set of stop words.
```
stopwords = set([
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by',
        'for', 'if', 'in', 'into', 'is', 'it',
        'no', 'not', 'of', 'on', 'or', 's', 'such',
        't', 'that', 'the', 'their', 'then', 'there', 'these',
        'they', 'this', 'to', 'was', 'will', 'with'
    ])
```
##### Punctuation
Queries are filtered using this punctuation marks regular expression.
```
punctuation = re.compile('[~`!@#$%^&*()+={\[}\]|\\:;"\',<.>/?]')
```
##### Stemming
Tokens are stemmed using the nltk **[PorterStemmer](https://www.nltk.org/_modules/nltk/stem/porter.html)** module to improve the quality of the search results.
```
ps = PorterStemmer()
token = ps.stem(token)
```
### Test Cases
1. Query: ```The Joker wreaks havoc on the people of Gotham```, Results: ```Found 162 results in 0.153 seconds```

### Author
**Jacob Wilkins**
* **[GitHub](https://github.com/JacobAWilkins/)**
* **[LinkedIn](https://www.linkedin.com/in/jacob-a-wilkins-cs/)**

# Movie Classifer Documentation

### Deployment Instructions
##### Online
http://jacobwilkins.pythonanywhere.com/classifer
##### Localhost
1. Install Flask:
```pip install flask```
2. Run Movifier:
```sudo python main.py```
   Wait for dataset to index movies. This will take a while unless you change the number of movies indexed to a lower number. The default is 1000. You can change this in main.py. Afterwards, you will see a message ``` * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)``` in the terminal.
3. In browser (localhost, port 5000):
```http://127.0.0.1:5000/classifer```
### Contributions & References
For the test classifer I used **[this](https://stackabuse.com/text-classification-with-python-and-scikit-learn/)** stackabuse article and **[this](https://github.com/ishmeetkohli/imdbGenreClassification/blob/master/utils.py)** GitHub repository as reference. Both of these solutions used a train test split to test the accuracy of the algorithm, but I modified it to only classify the data inputed by the user.
### Algorithms Explained
##### Preprocess
Before classification begins, the movie descriptions of the train/test data are preprocessed to remove all special characters, remove all single characters, remove all multiple spaces for singles spaces, and converted to lowercase. Finally, lemmantixation is performed.
##### Count Vectorizer
The vectorizer fitted and transformed the text descriptions of the train/test data (the train movie decriptions) to identify the data features and then converted them into an array to be used for classification.
##### Random Forest Classifier
The classifier fitted the data features to the movies genres and then used this to make a prediction of the genre for the test data. The prediction is displayed for the user.
### Challenge
My challenge was to transform the references that were designed for test train split into a system that used train data to classify a single test case. I resolved this issue by making the train and test data identical in form and used pandas to make Data Frames for the test/train allowing them to both have the same number of data features.

# Image Caption Generator Documentation

### Deployment Instructions
##### Online
http://jacobwilkins.pythonanywhere.com/caption
##### Localhost
1. Install Flask:
```pip install flask```
2. Run Movifier:
```sudo python main.py```
   Wait for dataset to index movies. This will take a while unless you change the number of movies indexed to a lower number. The default is 1000. You can change this in main.py. Afterwards, you will see a message ``` * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)``` in the terminal.
3. In browser (localhost, port 5000):
```http://127.0.0.1:5000/caption```

### Contributions & References
http://academictorrents.com/details/9dea07ba660a722ae1008c4c8afdd303b6f6e53b
