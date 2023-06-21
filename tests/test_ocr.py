
from multiocr import OcrEngine
import os
import pandas as pd
import json

image_file = "/Users/aravindh/Documents/GitHub/multiocr/tests/data/test-european.jpg"


all_ocr = [
    {
        "ocr_name":"tesseract",
        "config":{
            "lang": "eng",
            "config" : "--psm 6"
            }
    },
    {
        "ocr_name":"paddle_ocr",
        "config":{
            "lang":"en"
        }
    },
    {
        "ocr_name":"aws_textract",
        "config":{
            "region_name":os.getenv("region_name"),
            "aws_access_key_id":os.getenv("aws_access_key_id"),
            "aws_secret_access_key":os.getenv("aws_secret_access_key")
        }
    },
    {
        "ocr_name":"easy_ocr",
        "config":{
            "lang_list": ["en"]
        }
    }
]

for ocr in all_ocr:
    ocr_name = ocr["ocr_name"]
    ocr_config = ocr["config"]
    engine = OcrEngine(ocr_name, ocr_config)
    
    text_dict = engine.text_extraction(image_file)
    assert type(text_dict) == list
    assert len(text_dict)>1
    
    json_str = engine.text_extraction_to_json(text_dict)
    assert type(json_str) == str
    assert type(json.loads(json_str)) == list
    
    df = engine.text_extraction_to_df(text_dict)
    assert type(df) == pd.DataFrame
    assert len(df)>1
    
    plain_text = engine.extract_plain_text(text_dict)
    assert type(plain_text) == str
