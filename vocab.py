import csv
import nltk
from nltk.corpus import stopwords
import re
from typing import List, Dict, Tuple, Optional
import heapq

class Vocab:
    active_vocab: Dict[str, int]
    all_vocab: Dict[str, int]
    active_vocab_count: int
    news: List[Tuple[str, str, int]]
    changed: bool

    def __init__(self, true_file: str, fake_file: str, active_words_count: int = 1000):
        if not nltk.data.find('stopwords'):
            nltk.download('stopwords')
        
        self.active_vocab_count = active_words_count
        self.news = []
        self.all_vocab = {}
        self.active_vocab = {}

        with open(file= true_file, mode= 'r', encoding= "UTF-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.news.append((row['title'], row['text'], 1))
        
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
        TITLE_WEIGHT: float = 2

        for news in self.news:
            title, text, _ = news
            title, text = re.findall(r'\w', title.lower()), re.findall(r'\w', text.lower())
            
            for word in title:
                if word in stopword_set:
                    continue
                self.all_vocab[word] = self.all_vocab.get(word, 0) + TITLE_WEIGHT

            for word in text:
                if word in stopword_set:
                    continue
                self.all_vocab[word] = self.all_vocab.get(word, 0) + 1

    def generate_active_vocab(self) -> None:
        if len(self.all_vocab) == 0:
            return
        most_appeared = heapq.nlargest(
                n= self.active_vocab_count, 
                iterable= self.all_vocab.items(),
                key= lambda x: x[1])
        self.active_vocab = {x[0]: x[1] for x in most_appeared}
        self.changed = True
        
