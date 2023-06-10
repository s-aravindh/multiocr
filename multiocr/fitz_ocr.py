import io
import json
import pandas as pd
from PIL import Image
import fitz


class TextractOcr:
    def __init__(self, image_file):
        self.image_file = image_file

    def text_extraction(self):
        doc = fitz.open(self.image_file)
        page = doc[0]
        text_dict = {}
        for block in page.get_text("blocks"):
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"]
                    if text != "":
                        bbox = span["bbox"]
                        text_dict[text] = {
                            "text": text,
                            "confidence": 1.0,
                            "coordinates": {
                                "left": bbox[0],
                                "top": bbox[1],
                                "width": bbox[2] - bbox[0],
                                "height": bbox[3] - bbox[1],
                            },
                        }

        doc.close()
        return text_dict

    def text_extraction_to_json(self, text_dict):
        try:
            with open("output.json", "w") as f:
                json.dump(text_dict, f)
        except Exception as e:
            raise Exception(f"Error saving output to JSON file: {e}")

    def text_extraction_to_df(self, text_dict):
        rows = []
        for k, v in text_dict.items():
            rows.append(
                [
                    v["text"],
                    v["confidence"],
                    v["coordinates"]["left"],
                    v["coordinates"]["top"],
                    v["coordinates"]["width"],
                    v["coordinates"]["height"],
                ]
            )
        df = pd.DataFrame(
            rows,
            columns=["text", "confidence", "left", "top", "width", "height"],
        )

        try:
            df.to_csv("output.csv", index=False)
        except Exception as e:
            raise Exception(f"Error saving output to CSV file: {e}")

    def extract_plain_text(self, text_dict):
        plain_text = ""
        for k, v in text_dict.items():
            plain_text += v["text"] + "\n"
        try:
            with open("output.txt", "w") as f:
                f.write(plain_text)
        except Exception as e:
            raise Exception(f"Error saving output to plain text file: {e}")
