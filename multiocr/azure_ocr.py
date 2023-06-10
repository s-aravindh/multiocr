import io
import json
import pandas as pd
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image

class AzureOcr:
    def __init__(self, image_file, endpoint, key):
        self.image_file = image_file
        self.endpoint = endpoint
        self.key = key
        self.client = ComputerVisionClient(self.endpoint, CognitiveServicesCredentials(self.key))

    def text_extraction(self):
        with io.open(self.image_file, 'rb') as image_file:
            content = image_file.read()

        try:
            response = self.client.recognize_printed_text_in_stream(content=content)
            operation_id = response.headers['Operation-Location'].split('/')[-1]
        except Exception as e:
            raise Exception(f"Error recognizing text in image: {e}")
        
        response = None
        while response is None:
            response = self.client.get_read_operation_result(operation_id)
            if response.status in [TextOperationStatusCodes.failed, TextOperationStatusCodes.succeeded]:
                break
        
        if response.status == TextOperationStatusCodes.failed:
            raise Exception(f"Error recognizing text in image: {response.message}")
        
        text_dict = {}
        for text in response.recognition_result.lines:
            if text.text != '':
                coordinates = text.bounding_box
                text_dict[text.text] = {'text': text.text, 'confidence': text.confidence,
                                        'coordinates': {'left': coordinates[0], 'top': coordinates[1],
                                                        'width': coordinates[2] - coordinates[0],
                                                        'height': coordinates[5] - coordinates[1]}}
        
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
