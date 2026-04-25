import pytesseract
from PIL import Image, ImageDraw
import io


def run_ocr_and_annotate(image_file):
    """
    Futtatja a Tesseract OCR-t a képen.
    Visszatér:
      - full_text (str): detektált szöveg
      - annotated_bytes (BytesIO): piros téglalapokkal jelölt kép PNG-ként
    """
    img = Image.open(image_file).convert('RGB')
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    draw = ImageDraw.Draw(img)
    words = []

    for i in range(len(data['text'])):
        word = data['text'][i].strip()
        if not word or int(data['conf'][i]) < 0:
            continue
        words.append(word)
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        draw.rectangle([x, y, x + w, y + h], outline='red', width=2)

    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)

    return ' '.join(words), output
      