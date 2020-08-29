

import boto3
import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime

class Invite:
    
    def __init__(self):
        self.token = None
        self.companyID = None
        self.email = None
        self.expird = None

        
    def toDict(self):
        invitationDict = dict()
        invitationDict['token'] = self.token
        invitationDict['companyID'] = self.companyID
        invitationDict['email'] = self.email
        invitationDict['expird'] = self.expird
        
        return invitationDict
        
    @staticmethod
    def InviteFromRow(row):
        invitation = Invite()
        
        token = row['token']
        email = row['email']
        companyID = int(row['companyID'])
        ttl = int(row['ttl'])
        expird = datetime.datetime.utcfromtimestamp(ttl).strftime('%Y-%m-%d %H:%M:%S')
        invitation.token = token
        invitation.companyID = companyID
        invitation.email = email
        invitation.expird = expird

        return invitation
    
    def queryWithEmail(email):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('SellerlinxInviteToken')
        response = table.scan(FilterExpression=Key('email').eq(email))
        items = response['Items']

        invitations = list()
        for item in items:
            invitation = Invite.InviteFromRow(item)
            invitations.append(invitation.toDict())
        
        return invitations
    
    def queryWithCompanyID(companyID, limit=10, lastToken=None):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('SellerlinxInviteToken')
        
        if isinstance(companyID, int):
            companyID = str(companyID)
        
        
        if not lastTokenID is None:
            exclusiveStartKey = dict()
            exclusiveStartKey['token'] = lastToken
            exclusiveStartKey['companyID'] = companyID
            
            response = table.query(
                IndexName = 'companyID-index',
                KeyConditionExpression = Key('companyID').eq(companyID),
                ScanIndexForward = False,
                ExclusiveStartKey = exclusiveStartKey,
                Limit = limit
            )
        else:
            response = table.query(
                IndexName = 'companyID-index',
                KeyConditionExpression = Key('companyID').eq(companyID),
                ScanIndexForward = False,
                Limit = limit
            )
        
        items = response['Items']
        invitations = list()
        
        for item in items:
            invitation = Invite.InviteFromRow(item)
            invitations.append(invitation.toDict())
        
        return invitations
        
    @staticmethod
    def delete(token):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('SellerlinxInviteToken')
    
        res = table.delete_item(
                Key = {'token': token}
            )
        return 1
        
    