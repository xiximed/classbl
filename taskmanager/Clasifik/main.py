from .parser.parser import Parser
from .predictions.predictor import Predictor
from .utils.constants import DATASET_FILE_PATH
from .utils.constants import PREPARED_DATASET_FILE_PATH
from .tests.test_predict import test


class clasifr:
    TEXT = 'бл '

    if __name__ == '__main__':
        # parser = Parser()
        # parser.write_to_file()

        predictor = Predictor()
        predictor.train_data()
        res = predictor.get_sentiment_percentage(TEXT)
        if predictor.bad_words == {}:
            otv = 'Все ок'
        else:
            otv = f" {res['bad_words']}"


#reg = clasifr.otv
#print(reg)
