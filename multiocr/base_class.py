from abc import ABC


class OCR(ABC):

    def text_extraction(self):
        pass

    def text_extraction_to_json(self):
        pass

    def text_extraction_to_df(self):
        pass

    def extract_plain_text(self):
        pass