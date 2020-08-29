import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

class SES:
    def __init__(self, region="us-west-2"):
        self.configSet = None
        self.msg = dict()
        self.msg['status'] = 0
        self.msg['messages'] = None
        self.client = boto3.client('ses', region_name=region)

    @staticmethod
    def send(SENDER=None, RECIPIENT=None, SUBJECT=None, BODY_TEXT=None, BODY_HTML=None, CHARSET="UTF-8"):
        ses = SES()
        
        if SENDER is None:
            ses.msg['messages'] = 'Please provide a Sender'
            return ses.msg
        
        if RECIPIENT is None:
            ses.msg['messages'] = 'Please provide a Recipient'
            return ses.msg
        
        if SUBJECT is None:
            ses.msg['messages'] = 'Please provide a Subject'
            return ses.msg
        
        try:
            #Provide the contents of the email.
            response = ses.client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        except ClientError as e:
            ses.msg['status'] = -1
            ses.msg['messages'] = e.response['Error']['Message']
        else:
            ses.msg['status'] = 1
            ses.msg['messages'] = 'Email sent successfully.'
        
        return ses.msg
