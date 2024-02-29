import boto3
import json


def send_msg_to_sqs(queue_name, request_data):
    try:
        client = boto3.client('sqs', region_name='ca-central-1')

        queue_url = client.get_queue_url(QueueName=queue_name).get('QueueUrl')

        # send sqs message with the current date & time
        message = client.send_message(
            QueueUrl=queue_url,
            MessageBody=request_data
        )
        return {
            'statusCode': 200,
            'body': json.dumps(message, indent=2)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e), indent=2)
        }
