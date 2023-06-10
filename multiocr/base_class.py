from abc import ABC, abstractmethod


class OCR(ABC):

    @abstractmethod
    def text_extraction(self):
        pass

    @abstractmethod
    def text_extraction_to_json(self):
        pass
    
    @abstractmethod
    def text_extraction_to_df(self):
        pass
    
    @abstractmethod
    def extract_plain_text(self):
        pass