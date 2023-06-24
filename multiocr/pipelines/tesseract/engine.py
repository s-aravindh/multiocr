from multiocr.base_class import OCR
import json
import pytesseract
import pandas as pd
from PIL import Image
from typing import Union

class TesseractOcr(OCR):
    """
    The TextractOcr class takes an image file path as input. It has four methods:

    text_extraction(): This method extracts text from the image using Tesseract OCR and returns the text as a dictionary with the block IDs as keys and the text, confidence score, and bounding box coordinates as values.
    text_extraction_to_json(text_dict): This method takes the dictionary output from text_extraction() as input and saves it to a JSON file.
    text_extraction_to_df(text_dict): This method takes the dictionary output from text_extraction() as input and saves it to a Pandas DataFrame with columns for the text, confidence score, and bounding box coordinates.
    extract_plain_text(text_dict): This method takes the dictionary output from text_extraction() as input and saves the plain text to a text file.
    """
    def __init__(self, config:Union[dict, None]=None):
        self.config = config
        if not self.config:
            self.config = {
                "lang": "eng"
            }
        self.config.pop("output_type", None)
    
    def text_extraction(self, image_file):
        try:
            text = pytesseract.image_to_data( Image.open(image_file), output_type='dict', **self.config)
            self.raw_ocr = text
        except Exception as e:
            raise Exception(f"Error detecting text in image: {e}")
        
        text_dict = []
        
        for i in range(len(text['text'])):
            if text['conf'][i] > -1:
                text_dict.append({'text': text['text'][i], 'confidence': text['conf'][i],
                                'coordinates': {'xmin': text['left'][i], 'ymin': text['top'][i],
                                                'xmax': text['width'][i]+text['left'][i], 'ymax': text['height'][i]+text['top'][i]}})
        
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
    image_file = "/Users/aravindh/Documents/GitHub/multiocr/tests/data/test-european.jpg"
    config = {
        "lang": "eng",
        "config" : "--psm 6"
    }
    engine = TesseractOcr(config)
    text_dict = engine.text_extraction(image_file)
    json_op = engine.text_extraction_to_json(text_dict)
    df = engine.text_extraction_to_df(text_dict)
    plain_text = engine.extract_plain_text(text_dict)
    print()