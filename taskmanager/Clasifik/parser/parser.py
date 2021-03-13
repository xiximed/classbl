import csv
import json

from Clasifik.utils.preparation import TextPreparation
from Clasifik.utils.constants import DATASET_FILE_PATH
from Clasifik.utils.constants import PREPARED_DATASET_FILE_PATH


class Parser:
    def parse(self):
        with open(DATASET_FILE_PATH, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self._data = {
                'normal': [],
                'bad': [],
            }
            for row in reader:
                tp = TextPreparation(row['comment'])
                prepared_text = tp.prepare_text()
                # print(f"{prepared_text}: {row['toxic']}")
                if float(row['toxic']) == 0:
                    self._data['normal'].append({
                        'text': prepared_text,
                    })
                    print(f'NORMAL: {prepared_text}')
                elif float(row['toxic']) == 1:
                    self._data['bad'].append({
                        'text': prepared_text,
                    })
                    print(f'BAD: {prepared_text}')
                else:
                    print('Невалидный параметр')

    def write_to_file(self):
        self.parse()
        with open(PREPARED_DATASET_FILE_PATH, 'w',  encoding='utf-8') as outfile:
            json.dump(self._data, outfile, ensure_ascii=False)
