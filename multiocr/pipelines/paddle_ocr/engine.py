from multiocr.base_class import OCR
import json
import pandas as pd
import paddleocr
from PIL import Image
from paddleocr import draw_ocr
from typing import Union

class PaddleOcr:
    def __init__(self, config:Union[dict, None]=None):
        self.config = config
        if not self.config:
            self.config = {
            "lang":"en"
        }
        self.ocr = paddleocr.PaddleOCR(**self.config)

    def text_extraction(self, image_file):
        try:
            text = self.ocr.ocr(image_file)
            self.raw_ocr = text
        except Exception as e:
            raise Exception(f"Error detecting text in image: {e}")

        text_dict = []
        for line in text:
            for word in line:
                xmin = min([w[0] for w in word[0]])
                ymin = min([w[1] for w in word[0]])
                xmax = max([w[0] for w in word[0]])
                ymax = max([w[1] for w in word[0]])
                word_dict = {
                    "text": word[1][0],
                    "confidence": word[1][1],
                    "coordinates":{
                        "xmin":xmin,
                        "ymin":ymin,
                        "xmax":xmax,
                        "ymax":ymax
                        }
                    }
                text_dict.append(word_dict)

        return text_dict

    def text_extraction_to_json(self, text_dict):
        try:
            return json.dumps(text_dict)
        except Exception as e:
            raise Exception(f"Error converting text extraction to JSON: {e}")
        
    def text_extraction_to_df(self, text_dict):
        rows = []
        
        for v in text_dict:
            rows.append([v['text'], v['confidence'], v['coordinates']['xmin'], v['coordinates']['ymin'],
                         v['coordinates']['xmax'], v['coordinates']['ymax']])
        
        df = pd.DataFrame(rows, columns=['text', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax'])
        
        try:
            return df
        except Exception as e:
            raise Exception(f"Error converting text extraction to dataframe: {e}")
        
    def extract_plain_text(self, text_dict):
        plain_text = ''
        
        for v in text_dict:
            plain_text += v['text'] + ' '
        
        try:
            return plain_text
        except Exception as e:
            raise Exception(f"Error converting text extraction to plain text: {e}")

if __name__ == "__main__":
    config = {
        "lang":"en"
    }
    image_file = "/Users/aravindh/Documents/GitHub/multiocr/tests/data/test-european.jpg"
    ocr = PaddleOcr(config)
    data = ocr.text_extraction(image_file)
    json_data = ocr.text_extraction_to_json(data)
    plain_text_data = ocr.extract_plain_text(data)
    pd_df = ocr.text_extraction_to_df(data)
    print()