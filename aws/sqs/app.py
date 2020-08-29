import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError




def getQueue(queueName):
    sqs = boto3.resource('sqs', 
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name=REGION_NAME)
    queue = sqs.get_queue_by_name(QueueName=queueName)
    return queue

def getMessagesFromQueue(queue, maxNumberofMsg=1):
    messages = list()
    for message in queue.receive_messages(MaxNumberOfMessages=maxNumberofMsg, VisibilityTimeout=0, WaitTimeSeconds=5):
        msgBody = json.loads(message.body)
        
        # delete queue
        message.delete()
        messages.append(msgBody)
    return messages

