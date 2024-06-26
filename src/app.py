import os
import json
import hashlib
import boto3
import psycopg2 import connect, extras
from dotenv import load_dotenv


# loading environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# AWS settings from environment variables
AWS_REGION = os.getenv('AWS_REGION')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

# Setup AWS SQS client
sqs = boto3.client('sqs', region_name=AWS_REGION)


def fetch_messages():
    """Fetch messages from SQS queue"""
    response = sqs.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=10
    )
    return response.get('Messages',[])

def process_messages(messages):
    """ Process messages and return a list of processed records """
    processed_records = []
    for message in messages:
        body = json.loads(message['Body'])
        processed_record = {
            'user_id': body['user_id'],
            'device_type': body['device_type'],
            'masked_ip': hashlib.sha256(body['ip'].encode()).hexdigest(),
            'masked_device_id': hashlib.sha256(body['device_id'].encode()).hexdigest(),
            'locale': body['locale'],
            'app_version': body['app_version'],
            'create_date': body['create_date']
        }
        processed_records.append(processed_record)
    return processed_records


def save_records_to_db(records):
    """ Save processed records to PostgreSQL database """
    connection = connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()
    psycopg2.extras.execute_batch(cursor, """
    INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, [(record['user_id'], record['device_type'], record['masked_ip'], record['masked_device_id'], record['locale'], record['app_version'], record['create_date']) for record in records])
    connection.commit()
    cursor.close()
    connection.close()

def main():
    messages = fetch_messages()
    if messages:
        records = process_messages(messages)
        save_records_to_db(records)

if __name__ == '__main__':
    main()