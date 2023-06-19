# Multiocr
This package intends to give a common interface for multiple ocr backends

# Installation
```
pip install multiocr
```
# Supported OCR Backends

- Tesseract
- PaddleOCR
- Aws Textract
- EasyOCR

the output for all ocr backend will be simillar

# Code Example
**Tesseract**
```python
from multiocr import OcrEngine

config = {
    "lang": "eng",
    "config" : "--psm 6"   
}
image_file = "path/to/image.jpg"
engine = OcrEngine("tesseract", config)
text_dict = engine.text_extraction(image_file)
json = engine.text_extraction_to_json(text_dict)
df = engine.text_extraction_to_df(text_dict)
plain_text = engine.extract_plain_text(text_dict)
```
**PaddleOCR**
```python
from multiocr import OcrEngine

config = {
        "lang":"en"
    }
image_file = "path/to/image.jpg"
engine = OcrEngine("paddle_ocr", config)
text_dict = engine.text_extraction(image_file)
json = engine.text_extraction_to_json(text_dict)
df = engine.text_extraction_to_df(text_dict)
plain_text = engine.extract_plain_text(text_dict)
```
**Aws Textract**
```python
from multiocr import OcrEngine

config = {
    "region_name":os.getenv("region_name"),
    "aws_access_key_id":os.getenv("aws_access_key_id"),
    "aws_secret_access_key":os.getenv("aws_secret_access_key")
}
image_file = "path/to/image.jpg"

engine = OcrEngine("aws_textract", config)
text_dict = engine.text_extraction(image_file)
json = engine.text_extraction_to_json(text_dict)
df = engine.text_extraction_to_df(text_dict)
plain_text = engine.extract_plain_text(text_dict)
```

**EasyOCR**
```python
from multiocr import OcrEngine

config = {
    "lang_list": ["en"]
}
image_file = "path/to/image.jpg"
engine = OcrEngine("easy_ocr", config)
text_dict = engine.text_extraction(image_file)
json = engine.text_extraction_to_json(text_dict)
df = engine.text_extraction_to_df(text_dict)
plain_text = engine.extract_plain_text(text_dict)
print()
```

if you want to  access the output of each individual ocr engine in their own raw format, we can fetch it this way

```
raw_ocr_output = engine.engine.raw_ocr
```

**config** is the each ocr's input parameters and it should be python dictionary. if not given, it'll default to each respective libraries default parameters

the input parameters for each ocr differs, and you can look at its respective repo for all allowable parameters

Reference & Acknowlegements

- [Pytesseract](https://github.com/madmaze/pytesseract)
- [Tesseract](https://github.com/tesseract-ocr/tesseract)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [AWS Textract](https://docs.aws.amazon.com/textract/latest/dg/what-is.html)
- [EasyOCR](https://www.jaided.ai/easyocr/)