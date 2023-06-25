from multiocr.base_class import OCR
import boto3
import pandas as pd
import json
from typing import Union
from PIL import Image
import os

class AwsTextractOcr(OCR):
    """

    The TextractOcr class takes an image file path as input and an optional AWS region. It has four methods:

    text_extraction(): This method extracts text from the image using AWS Textract and returns the text as a dictionary with the block IDs as keys and the text, confidence score, and bounding box coordinates as values.
    text_extraction_to_json(text_dict): This method takes the dictionary output from text_extraction() as input and saves it to a JSON file.
    """

    def __init__(self, config: Union[dict, None]=None):

        self.config = config
        if not self.config:
            self.config = {
            "region_name":os.getenv("region_name"),
            "aws_access_key_id":os.getenv("aws_access_key_id"),
            "aws_secret_access_key":os.getenv("aws_secret_access_key")
        }
        self.client = boto3.client('textract', **self.config)
    
    def text_extraction(self, image_file):
        try:
            img = Image.open(image_file)
            with open(image_file, 'rb') as f:
                image_bytes = f.read()
        except Exception as e:
            raise Exception(f"Error reading image file: {e}")
        
        try:
            response = self.client.detect_document_text(Document={'Bytes': image_bytes})
            self.raw_ocr = response
            # with open("./aws_response.json","r") as f:
            #     response = json.  loads(f.read())
        except Exception as e:
            raise Exception(f"Error detecting text in image: {e}")
        
        text_dict = []
        
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                continue
                # text_dict[block['Id']] = {'text': block['Text'], 'confidence': block['Confidence'],
                #                           'coordinates': block['Geometry']['BoundingBox']}
            elif block['BlockType'] == 'WORD':
                if block['Id'] not in text_dict:
                    word = {'text': block['Text'], 'confidence': block['Confidence'],
                                              'coordinates': block['Geometry']['BoundingBox']}
                    w = word["coordinates"]["Width"]*img.width
                    h = word["coordinates"]["Height"]*img.height
                    x = word["coordinates"]["Left"]*img.width
                    y = word["coordinates"]["Top"]*img.height
                    word_dict = {
                        "text": word["text"],
                        "confidence": word["confidence"],
                        "coordinates": {
                            "xmin": x,
                            "ymin": y,
                            "xmax": x+w,
                            "ymax": y+h
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
    import os
    config = {
        "region_name":os.getenv("region_name"),
        "aws_access_key_id":os.getenv("aws_access_key_id"),
        "aws_secret_access_key":os.getenv("aws_secret_access_key")
    }
    image_file = "/Users/aravindh/Documents/GitHub/multiocr/tests/data/test-european.jpg"
    ocr = AwsTextractOcr(config)
    data = ocr.text_extraction(image_file)
    jsn_dt = ocr.text_extraction_to_json(data)
    pln_txt = ocr.extract_plain_text(data)
    df = ocr.text_extraction_to_df(data)
    print()