import string

import gensim
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np


class NLPFilter:
    def __init__(self, load_model=True, threshold=0.4, category_names=None, category_related_words=None, formula=0):
        if category_names is None:
            category_names = ["Business", "Sports", "Travel", "Politics", "IT", "Other"]
        if category_related_words is None:
            category_related_words = ['business work entrepreneur brand marketing client company product founder skill',
                                      'sport play fitness game running field ball',
                                      'travel trip visit tour holiday',
                                      'politics government diplomacy ministry election state country',
                                      'development programming software hardware system technology science robotics '
                                      'computers automation',
                                      'health lifestyle wellness']
        if formula == 0:
            self.formula = lambda x, y: np.divide(x.sum(axis=0), len(y)) + x.max(axis=0)
        else:
            self.aux_form = lambda x: np.where(x < 0.1, 0, x)
            self.formula = lambda x, y: self.aux_form(x).sum(axis=0)

        if load_model:
            self.model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin',
                                                                         binary=True)
        self.threshold = threshold
        self.category_names = category_names
        self.category_related_words = category_related_words

    def get_categories(self, to_predict):
        return [self.get_category(name) for name in to_predict]

    def get_categories_names(self):
        return self.category_names

    def get_category(self, title):
        tokens = word_tokenize(title)
        tokens = [w.lower() for w in tokens]
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        words = [word for word in stripped if word.isalpha()]
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        scores = np.zeros((len(words), len(self.category_related_words)))
        counter = -1
        for element in words:
            counter += 1
            for index in range(len(self.category_related_words)):
                try:
                    scores[counter][index] = max(
                        [self.model.similarity(possible_category, element) for possible_category in
                         self.category_related_words[index].split(' ')])
                except:
                    pass
        try:
            magic_formula = self.formula(scores, words)
        except:
            magic_formula = np.array([0])
        if max(magic_formula) > self.threshold:
            category = self.category_names[np.where(magic_formula == max(magic_formula))[0][0]]
        else:
            category = "Other"
        return title, category
