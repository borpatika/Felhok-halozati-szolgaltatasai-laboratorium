import pytesseract
from PIL import Image, ImageDraw
import io
import json
import pika
import os


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
    

def publish_image_event(image_obj):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.environ.get('RABBITMQ_HOST', 'rabbitmq')
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='image_events', durable=True)

    event = {
        "description": image_obj.description,
        "ocr_text": image_obj.ocr_text,
        "uploaded_at": str(image_obj.uploaded_at),
    }

    channel.basic_publish(
        exchange='',
        routing_key='image_events',
        body=json.dumps(event),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
    print(f"[INFO] Event published: {image_obj.description}")