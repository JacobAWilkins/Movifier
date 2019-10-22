# Movifier
Given a dataset of movie titles and descriptions, implements text search using BM25 to score, classifies movies by genre, and generates captions for movie scenes.

The text search takes a description of a movie and outputs a list of similar movies using BM25.

### Deployment Instructions
##### Online
http://jacobwilkins.pythonanywhere.com/home
##### Localhost
1. Install Flash:
```pip install flask```
2. Run Movifier:
```sudo python main.py```
   Wait for dataset to index movies. This will take a while unless you change the number of movies indexed to a lower number. The default is 1000. You can change this in main.py. Afterwards, you will see a message ``` * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)``` in the terminal.
3. In browser (localhost, port 5000):
```http://127.0.0.1:5000/```

### Contributions & References
* For text search, I used Toastdriven's **[microsearch](https://github.com/toastdriven/microsearch)** repository and added some optimizations. I optimized the text search by adding stemming capabilities using the **[nltk.stem.porter](https://www.nltk.org/_modules/nltk/stem/porter.html)** module. In addition, I added my own Okapi BM25 alogrithm based on the formulas from **[Wikipedia](https://en.wikipedia.org/wiki/Okapi_BM25#The_ranking_function)**
* For the Flask web app API, I used CoreyMschafer's **[Flask_Blog](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog)** repository as a starting point
* I developed an algorithm to highlight the query tokens in the text description results using regular expression. I used **[this post](https://www.saltycrane.com/blog/2007/10/using-pythons-finditer-to-highlight/)** from the Salty Crane blog as a reference

### Algorithms Explained
##### Documents
A field-based dictionary where the keys are field names and the values are the field's contents.
```
{
  "id": "movie-title",
  "text": "This is a movies description",
}
```
##### Inverted Index
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
##### Okapi BM25
For a given document, the [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25#The_ranking_function) algorithm, is calculated as
```
def bm25_relevance(self, terms, matches, current_doc, total_docs, curr_len, avg_len, b, k):
        score = 0

        for term in terms:
            idf = math.log((total_docs - matches[term] + 0.5) / (matches[term] + 0.5))
            score = score + (current_doc.get(term, 0) * idf * (k + 1)) / (current_doc.get(term, 0) + k * (1 - b + (b * (curr_len / avg_len))))

        return score
```
where "terms" is a list of terms, "matches" is the first dictionary returned from collect_results(self, terms), "current doc" is the second dictionary returned from collect_results(self, terms), "total_docs" is the total number of documents in the index, "curr_len" is the length of the current document, and "avg_len" is the average length of all the documents. "b" and "k" are used to modify scores to fall in a given range.
##### Other Optimizations
* Ngrams:
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
* Stop words:
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
* Punctuation:
Queries are filtered using this punctuation marks regular expression.
```
punctuation = re.compile('[~`!@#$%^&*()+={\[}\]|\\:;"\',<.>/?]')
```
* Stemming:
Tokens are stemmed using [PorterStemmer()](https://www.nltk.org/_modules/nltk/stem/porter.html) to improve the quality of the search results.
```
ps = PorterStemmer()
token = ps.stem(token)
```
### Test Cases
1. Query: ```The Joker wreaks havoc on the people of Gotham```, Results: ```Found 162 results in 0.153 seconds```
