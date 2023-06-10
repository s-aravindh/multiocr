import io
import json
import pandas as pd
from PIL import Image
from mmocr import MMOCR

class MMOcr:
    def __init__(self, image_file, config_file):
        self.image_file = image_file
        self.config_file = config_file
        self.mmocr = MMOCR(self.config_file)

    def text_extraction(self):
        image = Image.open(self.image_file)
        result = self.mmocr.recognize(image)

        text_dict = {}
        for box in result:
            text = box['text']
            if text != '':
                coordinates = box['box']
                text_dict[text] = {'text': text, 'confidence': box['score'],
                                   'coordinates': {'left': coordinates[0], 'top': coordinates[1],
                                                   'width': coordinates[2] - coordinates[0],
                                                   'height': coordinates[3] - coordinates[1]}}
        
        return text_dict

    def text_extraction_to_json(self, text_dict):
        try:
            with open('output.json', 'w') as f:
                json.dump(text_dict, f)
        except Exception as e:
            raise Exception(f"Error saving output to JSON file: {e}")
        
    def text_extraction_to_df(self, text_dict):
        rows = []
        
        for k, v in text_dict.items():
            rows.append([v['text'], v['confidence'], v['coordinates']['left'], v['coordinates']['top'],
                         v['coordinates']['width'], v['coordinates']['height']])
        
        df = pd.DataFrame(rows, columns=['text', 'confidence', 'left', 'top', 'width', 'height'])
        
        try:
            df.to_csv('output.csv', index=False)
        except Exception as e:
            raise Exception(f"Error saving output to CSV file: {e}")
        
    def extract_plain_text(self, text_dict):
        plain_text = ''
        
        for k, v in text_dict.items():
            plain_text += v['text'] + '\n'
        
        try:
            with open('output.txt', 'w') as f:
                f.write(plain_text)
        except Exception as e:
            raise Exception(f"Error saving output to plain text file: {e}")
