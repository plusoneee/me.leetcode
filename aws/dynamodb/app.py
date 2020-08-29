import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid
from datetime import datetime

''' 
Just a simple note for my simple work, haha. 
''' 

def scanItemsFromKey(tableName='MyDynamodbTable', region='ap-southeast-1', key='email', value='somebody_email'):
    email = value
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(tableName)
    response = table.scan(FilterExpression=Key(key).eq(email))
    return response['Items']


def getCountOfNotificationFromAtrr(tableName='NotificationsTable', region='ap-southeast-1', atrr='accountID', value='somebody_account_id'):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    accountID = value
    response = table.scan(FilterExpression=Attr(atrr).eq(accountID), Select="COUNT")
    count = response['Count']
    return count


def getNotificationItem(tableName='MyDynamodbTable', region='ap-southeast-1', key='notificationID', value='somebody_notificationID'):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    response = table.query(
        KeyConditionExpression=Key(key).eq(value)
    )
    return response

def deleteNotificationItem(tableName='MyDynamodbTable', region='ap-southeast-1', key='notificationID', value='somebody_notificationID'):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    response = table.delete_item(
        KeyConditionExpression=Key(key).eq(value)
    )
    return response

def queryNotificationFromIndex(tableName='NotificationsTable', region='ap-southeast-1', index='accountID-created-index', value='somebody_account_id', limit=10):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    notifications = list()
    accountID = value
    # index-name created by `accountID`, `created` two cols.
    indexName = 'accountID-created-index' 

    ''' Set exclusiveStartKey ''' 
    # query start from keys, exclusiveStartKey is a dict type.
    exclusiveStartKey = dict()
    exclusiveStartKey['notificationID'] = 'a_notificationID'
    exclusiveStartKey['accountID'] = accountID
    exclusiveStartKey['created'] = 'another_col_call_created'

    response = table.query(
                IndexName=indexName,
                KeyConditionExpression=Key('accountID').eq(accountID),
                ScanIndexForward=False,
                Limit=limit,
                ExclusiveStartKey=exclusiveStartKey)

    
    ''' Or Not set exclusiveStartKey '''
    response = table.query(
                IndexName=indexName,
                KeyConditionExpression=Key('accountID').eq(accountID),
                ScanIndexForward=False,
                Limit=limit)

    return response['Items']


def insertNotificationItem(tableName='NotificationsTable', region='ap-southeast-1'):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    now =  datetime.utcnow()
    expiry = datetime.utcnow() + datetime.timedelta(minutes=120)
    notificationID = uuid.uuid4()
    accountID = 'somebody_account_id'
    
    table.put_item( 
        Item= {
            'notificationID':str(notificationID),
            'accountID':accountID,
            'created':round(now.timestamp()),
            'ttl':str(round(expiry.timestamp()))
            }
        )
    return 1

def updateNotification(tableName='NotificationsTable', region='ap-southeast-1',  key='notificationID', value='somebody_notificationID'):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    notificationID = value
    now = datetime.utcnow()
    
    ''' For example: Set col `isRead` value is now '''
    response = table.update_item(
        Key={
            'notificationID': notificationID,
        },
        UpdateExpression="set isRead = :r",
        ExpressionAttributeValues={
            ':r': round(now.timestamp()),
        },
        ReturnValues="UPDATED_NEW"
    )
    return 1
    
