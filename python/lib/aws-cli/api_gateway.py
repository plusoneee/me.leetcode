
import os
import json
import datetime

class Method:
    def __init__(self):
        self.httpMethod = None
        self.authorizerID = None
        self.authorizerType = None
        self.apiKeyRequired = None
        self.integrationType = None
        self.integrationHttpMethod = None
        self.integrationUri = None
        self.integrationResponse = None

    def toDict(self):
        methodDict = dict()
        methodDict['httpMethod'] = self.httpMethod
        methodDict['authorizerID'] = self.authorizerID
        methodDict['authorizerType'] = self.authorizerType
        methodDict['apiKeyRequired'] = self.apiKeyRequired
        methodDict['integrationType'] = self.integrationType
        methodDict['integrationHttpMethod'] = self.integrationHttpMethod
        methodDict['integrationUri'] = self.integrationUri
        methodDict['integrationResponse'] = self.integrationResponse
        
        return methodDict

    @staticmethod
    def _create(_method):
        method = Method()
        method.httpMethod = _method['httpMethod']
        if 'authorizerId' in _method:
            method.authorizerID = _method['authorizerId']
        if 'authorizationType' in _method:
            method.authorizerType = _method['authorizationType']
        method.apiKeyRequired = _method['apiKeyRequired']

        if 'methodIntegration' in _method:
            methodIntegration = _method['methodIntegration']
            method.integrationType = methodIntegration['type']
            method.integrationHttpMethod = methodIntegration['httpMethod']
            method.integrationUri = methodIntegration['uri']
            if 'integrationResponses' in methodIntegration:
                method.integrationResponse = methodIntegration['integrationResponses']
    
        return method

    @staticmethod
    def get(restApiID, resourceID=None, httpMethod=None):

        if (resourceID is None) or (httpMethod is None):
            return None

        inputTuple = (restApiID, resourceID, httpMethod)

        cmd = ('aws apigateway get-method \
                --rest-api-id %s \
                --resource-id %s \
                 --http-method %s '%inputTuple)
        cmdOutput = os.popen(cmd).read()
        
        try:
            _method = json.loads(cmdOutput)
            method = Method._create(_method)
        except:
            return None

        return method

    @staticmethod
    def delete(restApiID, resourceID=None, httpMethod=None):

        if (resourceID is None) or (httpMethod is None):
            return 0

        inputTuple = (restApiID, resourceID, httpMethod)

        cmd = ('aws apigateway delete-method \
                --rest-api-id %s \
                --resource-id %s \
                 --http-method %s '%inputTuple)

        cmdOutput = os.popen(cmd).read()
        
        return 1

    @staticmethod
    def addAWSIntegration(restApiID, resourceID=None, method=None):
        
        if (resourceID is None) or (method is None):
            return None

        inputTuple = (restApiID, resourceID, method.httpMethod)

        # add aws integration on method
        cmd = ('aws apigateway put-integration \
                --rest-api-id %s \
                --resource-id %s \
                --http-method %s '%inputTuple)

        if not method.integrationType is None:
            cmd += (' --type %s' %method.integrationType)
        else:
            cmd += (' --type %s' %'AWS')

        if not method.integrationHttpMethod is None:
            cmd += (' --integration-http-method %s' %method.integrationHttpMethod)

        if not method.integrationUri is None:
            cmd += (' --uri %s' %method.integrationUri)

        cmdOutput = os.popen(cmd).read()
        method = Method.get(restApiID, resourceID, method.httpMethod)

        return 1

    @staticmethod
    def addAuthorizer(restApiID, resourceID=None, httpMethod=None, authorizer=None):
        
        # get original method info : integration lambda
        method = Method.get(restApiID, resourceID, httpMethod)
        if not method is None:
            # delete older resource method
            Method.delete(restApiID, resourceID, httpMethod)
            # add empty method
            updatedMethod = Method.insert(restApiID, resourceID, httpMethod, authorizer)
            # attach integration lambda function
            updatedMethod = Method.addAWSIntegration(restApiID, resourceID, method)

        return 1

    @staticmethod
    def insert(restApiID, resourceID=None, httpMethod=None, authorizer=None):
        
        cmd = ('aws apigateway put-method --no-api-key-required --rest-api-id %s' %restApiID)

        if not resourceID is None:
            cmd += (' --resource-id %s' %resourceID)

        if not httpMethod is None:
            cmd += (' --http-method %s' %httpMethod)

        if authorizer:
            if not authorizer.authorizerID is None:
                cmd += (' --authorization-type "CUSTOM" --authorizer-id %s' %authorizer.authorizerID)

        cmdOutput = os.popen(cmd).read()
        _method = json.loads(cmdOutput)

        method = Method._create(_method)

        return method        

class Resource:

    def __init__(self):
        self.resourceID = None
        self.parentID = None
        self.pathFull = None
        self.pathPart = None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, nextToken):
        self._token = nextToken

    def toDict(self):
        resourceDict = dict()
        resourceDict['resourceID'] = self.resourceID
        resourceDict['parentID'] = self.parentID
        resourceDict['pathFull'] = self.pathFull
        resourceDict['pathPart'] = self.pathPart

        return resourceDict

    def _create(_resource):
        resource = Resource()
        resource.resourceID = _resource['id']
        if 'parentId' in _resource:
            resource.parentID = _resource['parentId']
        if 'pathPart' is _resource:
            resource.pathPart = _resource['pathPart']
        resource.pathFull = _resource['path']
        return resource

    @staticmethod
    def insert(restApiID, parentID=None, pathPart=None):
        cmd = ('aws apigateway create-resource --rest-api-id %s' %restApiID)
        if not parentID is None:
            cmd += (' --parent-id %s' %parentID)
        if not pathPart is None:
            cmd += (' --path-part %s \"' %pathPart +'\"')

        cmdOutput = os.popen(cmd).read()
        _resource = json.loads(cmdOutput)
        resource = Resource._create(_resource)

        return resource

    @staticmethod
    def get(restApiID, resourceID=None):
        cmd = ('aws apigateway get-resource --rest-api-id %s --resource-id %s' %(restApiID, resourceID))

        cmdOutput = os.popen(cmd).read()
        
        try:
            _resource = json.loads(cmdOutput)
            resource = Resource._create(_resource)
        except:
            return None

        return resource

    @staticmethod
    def query(restApiID, token=None, limit=10):
        cmd = ('aws apigateway get-resources --rest-api-id %s --max-items %s' %(restApiID, limit))
        
        if not token is None:
            cmd +=(' --starting-token %s ' %token)
        
        cmdOutput = os.popen(cmd).read()
        _resources = json.loads(cmdOutput)
        
        resources = list()

        if 'NextToken' in _resources:
            Resource.token =  _resources['NextToken']
        else:
            Resource.token = None
        
        for _resource in _resources['items']:
            resource = Resource._create(_resource)
            resources.append(resource.toDict())
        return resources


class Authorizer:

    def __init__(self):
        
        self.authorizerID = None
        self.name = None
        self.uri = None
        self.identitySource = None
        self.type = None
        self.authorizerType = None
        
    def toDict(self):
        authorizerDict= dict()
        authorizerDict['authorizerID'] = self.authorizerID
        authorizerDict['name'] = self.name
        authorizerDict['uri'] = self.uri
        authorizerDict['identitySource'] = self.identitySource
        authorizerDict['type'] = self.type
        authorizerDict['authorizerType'] = self.authorizerType
        return authorizerDict

    @staticmethod
    def _create(_authorizer):
        authorizer = Authorizer()
        authorizer.authorizerID = _authorizer['id']
        authorizer.name = _authorizer['name']
        authorizer.uri = _authorizer['authorizerUri']
        authorizer.identitySource = _authorizer['identitySource']
        authorizer.type = _authorizer['type']
        authorizer.authType = _authorizer['authType']

        return authorizer

    @staticmethod
    def get(apiGatewayID=None, authorizerID=None):

        cmd = ('aws apigateway get-authorizer --rest-api-id %s ' %apiGatewayID)
        
        if not authorizerID is None:
            cmd += (' --authorizer-id %s ' %authorizerID)

        cmdOutput = os.popen(cmd).read()
        _authorizer = json.loads(cmdOutput)
        
        authorizer = Authorizer._create(_authorizer)

        return authorizer

    @staticmethod
    def query(apiGatewayID=None):
        cmd = ('aws apigateway get-authorizers --rest-api-id %s ' %apiGatewayID)
    
        cmdOutput = os.popen(cmd).read()
        _authorizers = json.loads(cmdOutput)
        
        authorizers = list()
        for _authorizer in _authorizers['items']:
            authorizer = Authorizer._create(_authorizer)
            authorizers.append(authorizer.toDict())

        return authorizers

    