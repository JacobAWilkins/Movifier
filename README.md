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

### Test Cases

### References
I based the text search algorithm on this code: https://github.com/toastdriven/microsearch. 
I used this code: https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog as a starting point for the development of the web app.
