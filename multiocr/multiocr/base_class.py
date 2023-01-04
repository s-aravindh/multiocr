from abc import ABC


class OCR(ABC):

    def image_to_str(self):
        pass

    def image_to_data(self):
        pass

    def image_to_json(self):
        pass