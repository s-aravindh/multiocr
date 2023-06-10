from base_class import OCR
import json
import pytesseract
import pandas as pd
from PIL import Image

class TesseractOcr(OCR):
    """
    The TextractOcr class takes an image file path as input. It has four methods:

    text_extraction(): This method extracts text from the image using Tesseract OCR and returns the text as a dictionary with the block IDs as keys and the text, confidence score, and bounding box coordinates as values.
    text_extraction_to_json(text_dict): This method takes the dictionary output from text_extraction() as input and saves it to a JSON file.
    text_extraction_to_df(text_dict): This method takes the dictionary output from text_extraction() as input and saves it to a Pandas DataFrame with columns for the text, confidence score, and bounding box coordinates.
    extract_plain_text(text_dict): This method takes the dictionary output from text_extraction() as input and saves the plain text to a text file.
    """
    def __init__(self, image_file):
        self.image_file = image_file
    
    def text_extraction(self):
        try:
            text = pytesseract.image_to_data(Image.open(self.image_file), output_type='dict')
        except Exception as e:
            raise Exception(f"Error detecting text in image: {e}")
        
        text_dict = []
        
        for i in range(len(text['text'])):
            if text['conf'][i] > -1:
                text_dict.append({'text': text['text'][i], 'confidence': text['conf'][i],
                                'coordinates': {'left': text['left'][i], 'top': text['top'][i],
                                                'width': text['width'][i], 'height': text['height'][i]}})
        
        return text_dict
    
    def text_extraction_to_json(self, text_dict):
        try:
            return json.dumps(text_dict)
        except Exception as e:
            raise Exception(f"Error saving output to JSON file: {e}")
        
    def text_extraction_to_df(self, text_dict):
        rows = []
        
        for v in text_dict:
            rows.append([v['text'], v['confidence'], v['coordinates']['left'], v['coordinates']['top'],
                         v['coordinates']['width'], v['coordinates']['height']])
        
        df = pd.DataFrame(rows, columns=['text', 'confidence', 'left', 'top', 'width', 'height'])
        
        try:
            return df
        except Exception as e:
            raise Exception(f"Error saving output to CSV file: {e}")
        
    def extract_plain_text(self, text_dict):
        plain_text = ''
        
        for v in text_dict:
            plain_text += v['text'] + ' '
        
        try:
            return plain_text
        except Exception as e:
            raise Exception(f"Error saving output to plain text file: {e}")

if __name__ == "__main__":
    ocr = TesseractOcr("/Users/aravindh/Documents/GitHub/multiocr/tests/data/test-european.jpg")
    data = ocr.text_extraction()
    json_data = ocr.text_extraction_to_json(data)
    plain_text_data = ocr.extract_plain_text(data)
    pd_df = ocr.text_extraction_to_df(data)
    print()