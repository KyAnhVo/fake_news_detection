# Fake news detection microservice server

## Dependency

- Python 3.9 at least
- torch, torchvision, torchaudio
- nltk
- numpy, scipy

NOTE: run "pip install torch torchvision torchaudio nltk numpy scipy" if needed

## Usage

python3 predict_fake_news.py
- spawns a microservice that can be sent text to/from

To: localhost:5000
Protocol: TCP

JSON request format (callee send to microserver):
{
    "func": "predict_real_fake",
    "title": "title of news",
    "text": "text of news"
}

JSON response format, success (microserver send to callee):
{
    "status": "ok",
    "result": "real" if news is real else "fake"
}

JSON response format, failure (microserver send to callee):
{
    "status": "error",
    "error": "error message"
}

## Reminder for AndroidSDK localhost:

Android emulators do not read from localhost address 127.0.0.1,
but instead should be sent to 10.0.0.2, i.e.:

```java
// WRONG
Socket socket = new Socket("localhost", 5000);

// CORRECT
Socket socket = new Socket("10.0.0.2", 5000);

```



## Idea (shouldn't matter unless prof specifically asks for this):

ML algorithm:

Using Bernoulli Naive Bayes, where we calculate
p(y|x) = p(x|y) * p(y) / p(x) (Bayes rule), but we maximize
p(x|y) * p(y) since p(x) is constant given input x. Assume all words are
independent given other words, i.e. p(x|y) = p(x|x1,x2,...,y)
(Naive Bayes Assumption). By maximizing the likelihood 
L(phi, p) = prod_i(p(x_i, y_i)), we arrive to the calculations
used in the code (please look at NB.py for context). Notice that
since we only use Bernoulli, words are only present/not present
and there is no count involved, which simplifies the whole expression.
This is, in general, very simple to what other people might use,
e.g. deep learning neural network implementations like CNN, Transformer.
But this is very efficient if we want to train the model to work on
phones where GPU usage is highly limited.

Data engineering:

To index the words, we recognize that the same word in title
has different weight than in text, we upper-cased all words in
title and lower-case all words in text. We then apply the 2000
most seen words to limit the scope of the program, and then sort
it from most appeared to least appeared, though the sorting should
not affect much since it is matmul at the end of the day. This is
relatively simple to what people in the real word uses, which they
use TF-IDF for characters, but should suffice for Bernoulli implementation
of Naive Bayes.
