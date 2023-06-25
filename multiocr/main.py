from multiocr.pipelines import AwsTextractOcr
from multiocr.pipelines import TesseractOcr
from multiocr.pipelines import PaddleOcr
from multiocr.pipelines import EasyOcr
from multiocr.base_class import OCR
from typing import Union

ENGINE_DICT = {"aws_textract":AwsTextractOcr, 
               "tesseract":TesseractOcr, 
               "paddle_ocr":PaddleOcr,
               "easy_ocr": EasyOcr }

avail_ocr_backends = list(ENGINE_DICT.keys())

class OcrEngineSelectionError(Exception):
    def __init__(self, msg:str) -> None:
        super().__init__()
        pass


class OcrEngine(OCR):
    def __init__(self, engine:str, config:Union[dict, None]=None) -> None:
        self.config = config
        self.engine = ENGINE_DICT[engine](self.config) if engine in avail_ocr_backends else None
        if self.engine is None:
            raise OcrEngineSelectionError(f"only these ocr backends are available : {avail_ocr_backends}")
    
    def text_extraction(self, image_file):
        text_dict = self.engine.text_extraction(image_file)
        return text_dict

    def text_extraction_to_json(self, text_dict):
        json_dict = self.engine.text_extraction_to_json(text_dict)
        return json_dict

    def text_extraction_to_df(self, text_dict):
        df = self.engine.text_extraction_to_df(text_dict)
        return df

    def extract_plain_text(self, text_dict):
        plain_text = self.engine.extract_plain_text(text_dict)
        return plain_text
   
if __name__ == "__main__":
    import os
    image_file = "/Users/aravindh/Documents/GitHub/multiocr/tests/data/test-european.jpg"
    paddle_config = {
         "lang":"en"
        }
    tess_config = {
        "lang": "eng",
        "config" : "--psm 6"   
    }
    aws_textract_config = {
        "region_name":os.getenv("region_name"),
        "aws_access_key_id":os.getenv("aws_access_key_id"),
        "aws_secret_access_key":os.getenv("aws_secret_access_key")
    }

    easy_ocr_config = {
        "lang_list": ["en"]
    }
    engine = OcrEngine("paddle_ocr", paddle_config)
    text_dict = engine.text_extraction(image_file)
    json = engine.text_extraction_to_json(text_dict)
    df = engine.text_extraction_to_df(text_dict)
    plain_text = engine.extract_plain_text(text_dict)
    print()
