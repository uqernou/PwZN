import re

from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor

regex = r'[.,:;?!]+'


class Histogram:
    def __init__(self, path, words=10, min_letters=0):
        self.text = ""
        self.path = path
        self.numer_of_words = words
        self.min_number_of_letters = min_letters
        self.list_tuple = []

    def load_file(self):
        loaded_file = open(self.path, 'r')
        self.text = loaded_file.read()

    def extract_array(self):
        total_list = list(filter(None, re.sub(regex, ' ', self.text).split(" ")))
        distinct_list = list(set(total_list))
        self.list_tuple = list((word, len(list(filter(lambda expresion: expresion == word, total_list)))) for word in distinct_list)
        self.list_tuple.sort(key=lambda tuples: tuples[1], reverse=True)
        filtered_list = list(filter(lambda exp: len(str(exp[0])) >= self.min_number_of_letters, self.list_tuple))
        return filtered_list[:self.numer_of_words]

    def pring_histogram(self):
        graph = Pyasciigraph()
        pattern = [Bla, Red, Gre, Yel, Blu, Pur, Cya, Whi]
        data = vcolor(self.extract_array(), pattern)
        graph = graph.graph('Histogram of words', data)
        for line in graph:
            print(line)
