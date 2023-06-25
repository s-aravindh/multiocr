import json
import pandas as pd
from easyocr import Reader
from typing import Union

class EasyOcr:
    def __init__(self, config: Union[dict, None]=None):
        self.config = config
        if not self.config:
            self.config = {
            "lang_list": ["en"]
        }
        self.ocr = Reader(**self.config)

    def text_extraction(self, image_file):
        try:
            result = self.ocr.readtext(image_file)
            self.raw_ocr = result
        except Exception as e:
            raise Exception(f"Error detecting text in image: {e}")

        text_dict = []
        for detection in result:
            text = detection[1]
            confidence = detection[2]
            xmin = int(min([w[0] for w in detection[0]]))
            ymin = int(min([w[1] for w in detection[0]]))
            xmax = int(max([w[0] for w in detection[0]]))
            ymax = int(max([w[1] for w in detection[0]]))
            word_dict = {
                "text": text,
                "confidence": confidence,
                "coordinates": {
                    "xmin": xmin,
                    "ymin": ymin,
                    "xmax": xmax,
                    "ymax": ymax
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
        "lang_list": ["en"]
    }
    image_file = "/Users/aravindh/Documents/GitHub/multiocr/tests/data/test-european.jpg"
    ocr = EasyOcr(config)
    data = ocr.text_extraction(image_file)
    json_data = ocr.text_extraction_to_json(data)
    plain_text_data = ocr.extract_plain_text(data)
    pd_df = ocr.text_extraction_to_df(data)
    print()
