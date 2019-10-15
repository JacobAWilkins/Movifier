# Movifier
Given a movie dataset, implements text search, classifier by genre, and image caption generator

### Deployment Instructions
1. Install Flash:
```pip install flask```
2. Run Movifier:
```sudo python main.py```
   Wait for dataset to index movies. You will see a message ``` * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)```
3. In browser (localhost, port 5000):
```http://127.0.0.1:5000/```

### Contributions
For text search, I used Toastdriven's microsearch (refer to References) and added some optimizations. Firstly, I added stemming capabilities using the nltk.stem library. In addition, I fixed a bug with the BM25 algorith that resulted in a divide by zero error.
For the Flask web app API, I used CoreyMschafer's Flask_Blog repository (refer to References) as a starting point.

### Algorithms Explained
- __init__: sets up the object & data directory
- setup(self): creates various data directories (must have read/write access)
- read_stats(self): reads the index-wide stats generated from stats.json
- write_stats(self, new_stats): writes the index-wide stats
##### BM25 Relevance
For a given document, the BM25 relevance is calculated as
```
score = b
for term in terms:
  if matches[term] == 0.0:
    continue
  idf = math.log((total_docs - matches[term] + 1.0) / matches[term]) / math.log(1.0 + total_docs)
  score = score + current_doc.get(term, 0) * idf / (current_doc.get(term, 0) + k)
return 0.5 + score / (2 * len(terms))
```
where "terms" is a list of terms, "matches" is the first dictionary returned from collect_results(self, terms), "current doc" is the second dictionary returned from collect_results(self, terms), and "total_docs" is the total number of documents in the index. Optionally, "b" is specifies the length of the documents and "k" is used to modify scores to fall in a given range.

### Test Cases

### References
I based the text search algorithm on this code: https://github.com/toastdriven/microsearch. 
I used this code: https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog as a starting point for the development of the web app.
