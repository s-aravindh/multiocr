import json
import pandas as pd
from PIL import Image
from typing import Union
from .doctr.models import ocr_predictor
import numpy as np

class DoctrOCR:
    def __init__(self, config: Union[dict, None] = None):
        self.config = config
        if not self.config:
            self.config = {}
        self.model = ocr_predictor(pretrained=True, **self.config)

    def text_extraction(self, image_file):
        try:
            if isinstance(image_file, str):
                image = np.array(Image.open(image_file).convert("RGB"))
            elif isinstance(image_file, Image):
                image = np.array(image_file.convert("RGB"))

            result = self.model([image])
            self.raw_ocr = result

            text_dict = []
            for page in result.pages:
                h,w = page.dimensions
                for block in page.blocks:
                    for line in block.lines:
                        for word in line.words:
                            text = word.value.strip()
                            if text:
                                confidence = word.confidence
                                box = word.geometry
                                text_dict.append({
                                    'text': text,
                                    'confidence': confidence,
                                    'coordinates': {
                                        'xmin': box[0][0]*w,
                                        'ymin': box[0][1]*h,
                                        'xmax': box[1][0]*w,
                                        'ymax': box[1][1]*h
                                    }
                                })
            return text_dict
        except Exception as e:
            raise Exception(f"Error detecting text in image: {e}")

    def text_extraction_to_json(self, text_dict):
        try:
            return json.dumps(text_dict)
        except Exception as e:
            raise Exception(f"Error converting text extraction to JSON: {e}")

    def text_extraction_to_df(self, text_dict):
        try:
            rows = []
            
            for v in text_dict:
                rows.append([v['text'], v['confidence'], v['coordinates']['xmin'], v['coordinates']['ymin'],
                            v['coordinates']['xmax'], v['coordinates']['ymax']])
            
            df = pd.DataFrame(rows, columns=['text', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax'])
            
            return df
        except Exception as e:
            raise Exception(f"Error converting text extraction to dataframe: {e}")
        
    def extract_plain_text(self, text_dict):
        try:
            plain_text = ''
            
            for v in text_dict:
                plain_text += v['text'] + ' '
            
            return plain_text
        except Exception as e:
            raise Exception(f"Error converting text extraction to plain text: {e}")

if __name__ == "__main__":
    image_file = "/Users/aravindh/Documents/GitHub/multiocr/tests/data/test-european.jpg"
    engine = DoctrOCR()
    text_dict = engine.text_extraction(image_file)
    json_op = engine.text_extraction_to_json(text_dict)
    df = engine.text_extraction_to_df(text_dict)
    plain_text = engine.extract_plain_text(text_dict)
    print()
