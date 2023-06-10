from base_class import OCR
import json
import pandas as pd
import paddleocr
from PIL import Image
from paddleocr import draw_ocr

class PaddleOcr:
    def __init__(self, image_file, lang="en", angle_classification=True):
        self.image_file = image_file
        self.lang = lang
        self.angle_clf = angle_classification
        self.ocr = paddleocr.PaddleOCR(use_angle_cls=self.angle_clf, lang=self.lang)

    def text_extraction(self):
        try:
            text = self.ocr.ocr(self.image_file, cls=self.angle_clf)
        except Exception as e:
            raise Exception(f"Error detecting text in image: {e}")

        text_dict = {}
        for line in text:
            for word in line:
                text_dict[word[0]] = {'text': word[1][0], 'confidence': word[1][1],
                                      'coordinates': {'left': word[0][0], 'top': word[0][1],
                                                      'width': word[0][2] - word[0][0], 'height': word[0][3] - word[0][1]}}
        
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

if __name__ == "__main__":
    ocr = PaddleOcr("/Users/aravindh/Documents/GitHub/multiocr/tests/data/test-european.jpg")
    data = ocr.text_extraction()
    json_data = ocr.text_extraction_to_json(data)
    plain_text_data = ocr.extract_plain_text(data)
    pd_df = ocr.text_extraction_to_df(data)
    print()