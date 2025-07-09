import csv
import nltk
from nltk.corpus import stopwords
import re
from typing import List, Dict, Tuple, Optional
import heapq

class Vocab:
    news: List[Tuple[str, str, int]]

    all_vocab: Dict[str, int]
    active_vocab: Dict[str, int]
    active_vocab_count: int

    word_index_map: Dict[str, int]
    changed: bool

    def __init__(self, true_file: str, fake_file: str, active_words_count: int = 1000):
        try:
            nltk.data.find('corpora/stopwords')
        except:
            nltk.download('stopwords')
        
        self.active_vocab_count = active_words_count
        self.news = []
        self.all_vocab = {}
        self.active_vocab = {}
        self.word_index_map = {}
        self.changed = False

        with open(file= true_file, mode= 'r', encoding= "UTF-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.news.append((row['title'], row['text'], 0))
        
        with open(file= fake_file, mode= 'r', encoding= "UTF-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.news.append((row['title'], row['text'], 1))

        self._generate_vocab()
        self.generate_active_vocab()

    
    def _generate_vocab(self) -> None:
        if len(self.news) == 0:
            return
        
        stopword_set = set(stopwords.words('english'))
        # characters in title holds more weight than characters in actual text

        
        for news in self.news:
            # Note: to distinguish between title words and text words,
            # all title words are capitalized (Hello -> HELLO)
            # and all text words are lowered (Hello -> hello)

            title, text, _ = news
            title, text = re.findall(r'\w+', title.upper()), re.findall(r'\w+', text.lower())

            for word in title:
                if word in stopword_set:
                    continue
                self.all_vocab[word] = self.all_vocab.get(word, 0) + 1

            for word in text:
                if word in stopword_set:
                    continue
                self.all_vocab[word] = self.all_vocab.get(word, 0) + 1

    def generate_active_vocab(self) -> None:
        if len(self.all_vocab) == 0:
            return
        word_index_map = heapq.nlargest(n= self.active_vocab_count, iterable= self.all_vocab.items(), key= lambda x: x[1])
        self.active_vocab = {x[0]: x[1] for x in word_index_map}
        self.word_index_map = {x[0] : index for index, x in enumerate(word_index_map)}
        self.changed = False
        
    def get_training_data(self) -> Tuple[List[List[int]], List[int]]:
        if self.changed:
            self.generate_active_vocab()
        x, y = [], []
        for title, text, is_fake_news in self.news:
            x_curr: List[int] = [0 for _ in range(self.active_vocab_count)]
            y_curr: int = is_fake_news

            title, text = re.findall(r'\w+', title.upper()), re.findall(r'\w+', text.lower())
            for word in title + text:
                if word in self.word_index_map:
                    x_curr[self.word_index_map[word]] = 1
            x.append(x_curr)
            y.append(y_curr)

        return x, y
    
    # note: news is a {'title': <title>, 'text': <text>} json turned dict
    def get_parameter(self, news: Dict[str, str]) -> List[int]:
        if self.changed:
            self.generate_active_vocab()
        words = re.findall(r'\w+', news['title'].upper()) + re.findall(r'\w+', news['text'].lower())
        lst = [0 for _ in range(self.active_vocab_count)]

        for word in words:
            if word in self.word_index_map:
                lst[self.word_index_map[word]] = 1

        return lst



