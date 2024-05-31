import json
import time
from enum import Enum
import pika
import requests
from requests.auth import HTTPBasicAuth

class Status(Enum):
    STARTED = 'started'
    RUNNING = 'running'
    FINISHED = 'finished'
    CRASHED = 'crashed'

class ScriptListenerHelper:
    @staticmethod
    def create_connection():
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
            return connection
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ server: {e}")
            return None

    @staticmethod
    def create_queue(channel, queue_name):
        channel.queue_declare(queue=queue_name)

    @staticmethod
    def send_message(queue_name, message):
        connection = ScriptListenerHelper.create_connection()
        channel = connection.channel()
        ScriptListenerHelper.create_queue(channel, queue_name)

        properties = pika.BasicProperties(
            timestamp=int(time.time()),  # Unix timestamp formatında zaman damgası
            content_type='text/plain',
            delivery_mode=2  # Kalıcı mesajlar
        )

        channel.basic_publish(exchange='', routing_key=queue_name, body=message , properties=properties)
        print(f" [x] Sent '{message}' to queue '{queue_name}'")
        connection.close()

    @staticmethod
    def receive_message(queue_name):
        connection = ScriptListenerHelper.create_connection()
        if connection is None:
            print("Connection failed. No messages received.")
            return None

        channel = connection.channel()
        ScriptListenerHelper.create_queue(channel, queue_name)
        messages = []
        message_bodies = []

        while True:
            method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
            if method_frame:
                message_info = {
                    "body": body,
                    "delivery_tag": method_frame.delivery_tag,
                    "exchange": method_frame.exchange,
                    "routing_key": method_frame.routing_key,
                    "content_type": header_frame.content_type if header_frame else None,
                    "content_encoding": header_frame.content_encoding if header_frame else None,
                    "headers": header_frame.headers if header_frame else None,
                    "delivery_mode": header_frame.delivery_mode if header_frame else None,
                    "priority": header_frame.priority if header_frame else None,
                    "correlation_id": header_frame.correlation_id if header_frame else None,
                    "reply_to": header_frame.reply_to if header_frame else None,
                    "expiration": header_frame.expiration if header_frame else None,
                    "message_id": header_frame.message_id if header_frame else None,
                    "timestamp": header_frame.timestamp if header_frame else None,
                    "type": header_frame.type if header_frame else None,
                    "user_id": header_frame.user_id if header_frame else None,
                    "app_id": header_frame.app_id if header_frame else None,
                }
                messages.append(message_info)
                message_bodies.append(body)
                print(f" [x] Received message: {message_info['body']}")
            else:
                break

        connection.close()

        if not messages:
            return "Tüm mesajlar okundu veya kuyruk boş."

        return message_bodies

    @staticmethod
    def list_queues():
        url = 'http://localhost:15672/api/queues'
        response = requests.get(url, auth=HTTPBasicAuth('guest', 'guest'))
        if response.status_code == 200:
            queues = response.json()
            return [queue['name'] for queue in queues]
        else:
            return f"Failed to retrieve queues: {response.status_code}"


    @staticmethod
    def delete_queue(queue_name):
        connection = ScriptListenerHelper.create_connection()
        channel = connection.channel()
        channel.queue_delete(queue=queue_name)
        print(f" [x] Deleted queue '{queue_name}'")
        connection.close()


    @staticmethod
    def script_listener(script_name='', status='', output=None, error=None):
        try:
            message = {
                "script_name": f"{script_name}.py" if script_name else "No script name provided",
                "status": status,
                "timestamp": int(time.time()),
                "output": output,
                "error": error
            }
            json_message =json.dumps(message)
            ScriptListenerHelper.send_message('script_listener', json_message)
            print("script_listener kuyruğuna mesaj gönderildi.")
            return message
        except Exception as e:
            print(f"Error: {e}")
            pass

    @staticmethod
    def error_catcher_queue():
        messages = ScriptListenerHelper.receive_message('script_listener')

        if isinstance(messages, list):
            for message in messages:
                message_dict = json.loads(message)
                print(f"Script Name: {message_dict['script_name']}")
                print(f"Status: {message_dict['status']}")
                print(f"Timestamp: {message_dict['timestamp']}")
                print(f"Output: {message_dict['output']}")
                print(f"Error: {message_dict['error']}")
                print("\n")
        else:
            print("No messages received from script_listener queue.")


