import json
import os
import logging
import socket
from typing import Any
import boto3
from boto3.exceptions import Boto3Error
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)

queue_url = os.getenv('QUEUE_URL')
region = os.getenv('AWS_REGION')
max_msg_count = int(os.getenv('MAX_MSG_COUNT', 1))

if not queue_url:
    logging.fatal("QUEUE_URL environment variable is required")
    raise ValueError("QUEUE_URL environment variable is required")

if not region:
    logging.fatal("AWS_REGION environment variable is required")
    raise ValueError("AWS_REGION environment variable is required")

hostname = socket.gethostname()

def process_message(client: Any) -> None:
    try:
        response = client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_msg_count,
            WaitTimeSeconds=10
        )
        messages = response.get('Messages', [])
        if messages:
            for message in messages:
                logging.info("Received message: %s", message['Body'])
                client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
                logging.info("Message deleted")
        else:
            logging.info("No message(s) received")
    except (Boto3Error, ClientError) as e:
        logging.error("Failed to receive message: %s", e)

def lambda_handler(event: dict, context: Any) -> dict:
    try:
        client = boto3.client('sqs', region_name=region)
        process_message(client)
        return {
            'statusCode': 200,
            'body': 'Message received successfully'
        }
    except Exception as e:
        logging.error("Lambda function error: %s", e)
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }

if __name__ == '__main__':
    client = boto3.client('sqs', region_name=region)
    process_message(client)
