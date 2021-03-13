import re

from .stemmer_porter_algorithm import Stemmer


class TextPreparation:
    def __init__(self, text):
        self._st = Stemmer()
        self._text = text

    def strip_and_convert_to_lower(self):
        self._text = self._text.lower().strip()

    def remove_non_letter_characters(self):
        self._text = re.sub(r'([^\s\w]|_)+', '', self._text)

    def stemmer(self):
        words = self._text.split()
        self._text = ''
        new_words = []
        for word in words:
            new_words.append(self._st.stem(word))
        self._text = ' '.join(new_words)

    def prepare_text(self):
        self.strip_and_convert_to_lower()
        self.remove_non_letter_characters()
        self.stemmer()
        return self._text
