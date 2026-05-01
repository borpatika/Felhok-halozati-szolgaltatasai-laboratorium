import pika
import json
import time
import os
import psycopg2


def get_subscribers():
    conn = psycopg2.connect(
        dbname=os.environ.get('DB_NAME', 'ocrdb'),
        user=os.environ.get('DB_USER', 'ocruser'),
        password=os.environ.get('DB_PASSWORD', 'ocrpassword'),
        host=os.environ.get('DB_HOST', 'postgres-service'),
    )
    cur = conn.cursor()
    cur.execute("SELECT email FROM images_subscriber;")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]


def send_to_subscribers(data):
    subscribers = get_subscribers()
    for email in subscribers:
        print(f"=== NOTIFICATION -> {email} ===")
        print(f"Desc: {data.get('description')}")
        print(f"OCR: {data.get('ocr_text')}")
        print("==============================")


def callback(ch, method, properties, body):
    data = json.loads(body)
    send_to_subscribers(data)


def start_worker():
    host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host)
            )
            channel = connection.channel()
            channel.queue_declare(queue='image_events', durable=True)
            channel.basic_consume(
                queue='image_events',
                on_message_callback=callback,
                auto_ack=True
            )
            print("[INFO] Worker started, waiting for messages...")
            channel.start_consuming()
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}, retrying in 5s...")
            time.sleep(5)


if __name__ == "__main__":
    start_worker()