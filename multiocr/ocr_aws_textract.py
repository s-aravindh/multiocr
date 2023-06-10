from base_class import OCR
import boto3
import pandas as pd
import json

class AwsTextractOcr(OCR):
    """

    The TextractOcr class takes an image file path as input and an optional AWS region. It has four methods:

    text_extraction(): This method extracts text from the image using AWS Textract and returns the text as a dictionary with the block IDs as keys and the text, confidence score, and bounding box coordinates as values.
    text_extraction_to_json(text_dict): This method takes the dictionary output from text_extraction() as input and saves it to a JSON file.
    """

    def __init__(self, image_file, aws_access_key_id, aws_secret_access_key, aws_region):
        self.image_file = image_file
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region
        self.client = boto3.client('textract', region_name=aws_region,
                                   aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    def text_extraction(self):
        try:
            with open(self.image_file, 'rb') as f:
                image_bytes = f.read()
        except Exception as e:
            raise Exception(f"Error reading image file: {e}")
        
        try:
            response = self.client.detect_document_text(Document={'Bytes': image_bytes})
        except Exception as e:
            raise Exception(f"Error detecting text in image: {e}")
        
        text_dict = {}
        
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text_dict[block['Id']] = {'text': block['Text'], 'confidence': block['Confidence'],
                                          'coordinates': block['Geometry']['BoundingBox']}
            elif block['BlockType'] == 'WORD':
                if block['Id'] not in text_dict:
                    text_dict[block['Id']] = {'text': block['Text'], 'confidence': block['Confidence'],
                                              'coordinates': block['Geometry']['BoundingBox']}
                else:
                    text_dict[block['Id']]['text'] += ' ' + block['Text']
                    text_dict[block['Id']]['confidence'] = max(text_dict[block['Id']]['confidence'],
                                                               block['Confidence'])
        
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
            rows.append([v['text'], v['confidence'], v['coordinates']['Left'], v['coordinates']['Top'],
                         v['coordinates']['Width'], v['coordinates']['Height']])
        
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
    ocr = AwsTextractOcr("/Users/aravindh/Documents/GitHub/multiocr/tests/data/test-european.jpg",
                         aws_access_key_id="AKIA6DVKS7O4G2SCW2PJ", aws_secret_access_key="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", aws_region="us-east-1")
    data = ocr.text_extraction()
    ocr.text_extraction_to_json(data)
    ocr.extract_plain_text(data)
    ocr.text_extraction_to_df(data)