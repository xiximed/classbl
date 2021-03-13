import json
import math
import logging

from Clasifik.utils.constants import PREPARED_DATASET_FILE_PATH
from Clasifik.utils.preparation import TextPreparation


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


class Predictor:
    COUNT_DIGITS_AFTER_DOT = 3
    
    def __init__(self):
        self._bad_dict = {}
        self._normal_dict = {}

        self._bad_frequencies = 0
        self._normal_frequencies = 0

        self.bad_words = {}
        
        with open(PREPARED_DATASET_FILE_PATH) as file:
            self._data = json.loads(file.read())

    # сама проверка текста
    def get_sentiment_percentage(self, testing_text):
        common_prepared_words_dict = self.prepare_text(testing_text)
        # количество уникальных слов в обеих выборках
        count_unique_keys = self.get_count_unique_keys()
        # подсчет шанса что bad (не вероятностное пространство)
        res_bad = self.get_probability_bad(common_prepared_words_dict, count_unique_keys)
        # подсчет шанса что normal (не вероятностное пространство)
        res_normal = self.get_probability_normal(common_prepared_words_dict, count_unique_keys)

        prob_bad = self.formation_of_probabilistic_space(res_bad, res_normal)
        prob_normal = self.formation_of_probabilistic_space(res_normal, res_bad)

        if prob_bad > prob_normal:
            prob_bad = truncate(prob_bad, self.COUNT_DIGITS_AFTER_DOT)
            prob_normal = truncate(1 - prob_bad, self.COUNT_DIGITS_AFTER_DOT)
        else:
            prob_normal = truncate(prob_normal, self.COUNT_DIGITS_AFTER_DOT)
            prob_bad = truncate(1 - prob_normal, self.COUNT_DIGITS_AFTER_DOT)

        self.normalize_bad_words()

        return {
            'probability_bad': prob_bad,
            'probability_normal': prob_normal,
            'bad_words': self.bad_words,
        }

    # нормализация насколько слово плохое/хорошее в диапазоне от 0 до 1
    def normalize_bad_words(self):
        if not self.bad_words.values():
            return
        max_val = max(self.bad_words.values())
        min_val = min(self.bad_words.values())
        for key, value in self.bad_words.items():
            try:
                self.bad_words[key] = (value - min_val) / (max_val - min_val)
            except ZeroDivisionError:
                self.bad_words[key] = 1

    # подготовка тренировочных данных
    def train_data(self):
        for bad_data in self._data['bad']:
            self._bad_frequencies += 1
            text = bad_data['text']
            words = text.split()
            for word in words:
                if word in self._bad_dict:
                    self._bad_dict[word] += 1
                else:
                    self._bad_dict[word] = 1
        for normal_data in self._data['normal']:
            self._normal_frequencies += 1
            text = normal_data['text']
            words = text.split()
            for word in words:
                if word in self._normal_dict:
                    self._normal_dict[word] += 1
                else:
                    self._normal_dict[word] = 1

    def prepare_text(self, text):
        prepared_words = []
        words = text.lower().split()
        for word in words:
            tp = TextPreparation(word)
            prepared_words.append({
                'common': word,
                'prepared': tp.prepare_text(),
            })
        return prepared_words

    # заполнение словарей словами, которые принадлежат к конкретной категории
    def fill_dictionary(self):
        pass

    # Подсчет кол-ва уникальных слов во всей выборке
    def get_count_unique_keys(self):
        key_list_normal = list(self._normal_dict.keys())
        key_list_bad = list(self._bad_dict.keys())
        key_list_bad += key_list_normal
        key_list_bad = list(set(key_list_bad))
        return len(key_list_bad)

    # Вычисление вероятности, что сообщение bad
    def get_probability_bad(self, words, count_unique_keys):
        W = []
        for word in words:
            if word['prepared'] in self._bad_dict.keys():
                W.append(self._bad_dict[word['prepared']])
                # процент насколко слово плохое
                if word['prepared'] in self._normal_dict.keys():
                    count_normal_words_including = self._normal_dict[word['prepared']]
                else:
                    count_normal_words_including = 0.1
                how_word_is_bad = self._bad_dict[word['prepared']] / count_normal_words_including
                if how_word_is_bad > 1:
                    self.bad_words[word['common']] = how_word_is_bad
            else:
                W.append(0)

        prob_bad = math.log(self._bad_frequencies / (self._bad_frequencies + self._normal_frequencies))
        for w in W:
            prob_bad += math.log((1 + w) / (count_unique_keys + len(self._bad_dict)))
        return prob_bad

    # Вычисление вероятности, что сообщение bad
    def get_probability_normal(self, words, count_unique_keys):
        W = []
        for word in words:
            if word['prepared'] in self._normal_dict.keys():
                W.append(self._normal_dict[word['prepared']])
            else:
                W.append(0)

        prob_normal = math.log(self._normal_frequencies / (self._normal_frequencies + self._bad_frequencies))
        for w in W:
            prob_normal += math.log((1 + w) / (count_unique_keys + len(self._bad_dict)))
        return prob_normal

    # Формирование вероятностного пространства
    def formation_of_probabilistic_space(self, a, b):
        # TODO: костыль, возвращающий 50 на 50 в случае деления на 0. Разобраться почему так происходит
        try:
            return math.exp(a) / (math.exp(a) + math.exp(b))
        except ZeroDivisionError:
            logging.error("\n================\n\DIVIDING BY ZERO\n================\n")
            return 0.5
