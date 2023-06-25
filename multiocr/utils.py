from PIL import Image, ImageDraw
# import fitz

def draw_bounding_boxes(image_file, text_dict):
    # Open the image file
    image = Image.open(image_file).convert("RGBA")
    # Initialize the drawing context
    draw = ImageDraw.Draw(image)
    
    # Draw a green bounding box around each word
    for v in text_dict:
        left = v["coordinates"]["xmin"]
        top = v["coordinates"]["ymin"]
        right = v["coordinates"]["xmax"]
        bottom = v["coordinates"]["ymax"]
        draw.rectangle((left, top, right, bottom), outline='green', width=2)

    # Return the image with bounding boxes drawn over the words
    return image


def is_digital_page(pdf_path, page_num):
    # Open the PDF file and select the specified page
    with fitz.open(pdf_path) as doc:
        page = doc[page_num]

        # Check if the page is a scanned image
        if page.is_image:
            return False
        
        # Check if the page contains any text
        text = page.get_text()
        if text.strip():
            # Check if the text is really text or binary contents
            if text.isprintable():
                return True
            else:
                return False
        
        # If the page is not a scanned image and does not contain text, it's likely a digital page
        return True
