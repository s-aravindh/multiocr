import io
import json
import pandas as pd
from google.cloud import vision
from PIL import Image

class GoogleVisionOcr:
    def __init__(self, image_file):
        self.image_file = image_file
        self.client = vision.ImageAnnotatorClient()

    def text_extraction(self):
        with io.open(self.image_file, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        try:
            response = self.client.text_detection(image=image)
            text_annotations = response.text_annotations
        except Exception as e:
            raise Exception(f"Error detecting text in image: {e}")
        
        text_dict = {}
        for text in text_annotations:
            if text.description != '':
                vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
                text_dict[text.description] = {'text': text.description, 'confidence': text.confidence,
                                               'coordinates': {'left': vertices[0][0], 'top': vertices[0][1],
                                                               'width': vertices[2][0] - vertices[0][0],
                                                               'height': vertices[2][1] - vertices[0][1]}}
        
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
