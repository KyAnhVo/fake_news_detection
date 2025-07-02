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

    param_list: Dict[str, int]
    changed: bool

    def __init__(self, true_file: str, fake_file: str, active_words_count: int = 1000, title_weight: int = 2):
        if not nltk.data.find('stopwords'):
            nltk.download('stopwords')
        
        self.TITLE_WEIGHT = title_weight
        self.active_vocab_count = active_words_count
        self.news = []
        self.all_vocab = {}
        self.active_vocab = {}
        self.param_list = {}

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
            title, text = re.findall(r'\w', title.upper()), re.findall(r'\w', text.lower())
            
            for word in title:
                if word in stopword_set:
                    continue
                self.all_vocab[word] = 1

            for word in text:
                if word in stopword_set:
                    continue
                self.all_vocab[word] = 1

    def generate_active_vocab(self) -> None:
        if len(self.all_vocab) == 0:
            return
        param_list = heapq.nlargest(n= self.active_vocab_count, iterable= self.all_vocab.items(), key= lambda x: x[1])
        self.active_vocab = {x[0]: x[1] for x in param_list}
        self.param_list = {x[0] : index for index, x in enumerate(param_list)}
        
    def get_training_data(self) -> Tuple[List[List[int]], List[int]]:
        if self.changed:
            self.generate_active_vocab()
        x, y = [], []
        for title, text, is_fake_news in self.news:
            x_curr: List[int] = [0 for _ in range(self.active_vocab_count)]
            y_curr: List[int] = [is_fake_news]
            # process title
            for word in title + text:
                if word in self.param_list:
                    x_curr[self.param_list[word]] = 1
            x.append(x_curr)
            y.append(y_curr)

        return x, y
