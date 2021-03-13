import csv

from Clasifik.predictions.predictor import Predictor
from Clasifik.utils.constants import DATASET_FILE_PATH


def test():
    with open(DATASET_FILE_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            predictor = Predictor()
            predictor.train_data()
            res = predictor.get_sentiment_percentage(row['comment'])
            print(
                f"TEXT: {row['comment']}"
                f"PROB_BAD: {res['probability_bad']}\n"
                f"PROB_NORMAL: {res['probability_normal']}\n"
                f"BAD_WORDS: {res['bad_words']}\n"
            )
