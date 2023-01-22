from base_class import OCR
from pytesseract import image_to_string, image_to_data, image_to_boxes, image_to_osd


class TesseractOCR(OCR):

    def __init__(self, image) -> None:
        super().__init__()
        self.image = image

    def image_to_str(self):
        ...
        

    def image_to_data(self):
        ...

    def image_to_json(self):
        ...