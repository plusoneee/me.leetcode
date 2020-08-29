import os
import json
import csv
import datetime

class LambdaFunction:
    def __init__(self):
        self.name = None
        self.arn = None
        self.role = None
        self.layers = list()
        self.memorySize = None
        self.codeSize = None
        self.updated = None
        self._token = None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, nextToken):
        self._token = nextToken

    def toDict(self):
        lambdaDict = dict()
        lambdaDict['name'] = self.name
        lambdaDict['arn'] = self.arn
        lambdaDict['role'] = self.role
        lambdaDict['layers'] = self.layers
        lambdaDict['memorySize'] = self.memorySize
        lambdaDict['codeSize'] = self.codeSize
        lambdaDict['updated'] = self.updated

        return lambdaDict

    @staticmethod
    def create(_lambda):
        function = LambdaFunction()
        function.name = _lambda['FunctionName']
        function.arn = _lambda['FunctionArn']
        function.role = _lambda['Role']
        function.memorySize = _lambda['MemorySize']
        function.codeSize = _lambda['CodeSize']

        function.layers = list()
        if 'Layers' in _lambda:
            for layer in _lambda['Layers']:
                function.layers.append(layer['Arn'])
        function.updated = _lambda['LastModified']
        return function

    @staticmethod
    def get(name=None):
        if not name is None:
            cmd = ('aws lambda get-function --function-name %s' %name)
            cmdOutput = os.popen(cmd).read()
            _lambda = json.loads(cmdOutput)
            function = LambdaFunction.create(_lambda['Configuration'])

            return function

        return None

    @staticmethod
    def query(token=None, limit=10):
        
        cmd = ('aws lambda list-functions --max-items %s' %limit)
        if not token is None:
            cmd +=(' --starting-token %s ' %token)

        cmdOutput = os.popen(cmd).read()
        lambdaFunction = json.loads(cmdOutput)

        functions = list()

        for _lambda in lambdaFunction['Functions']:
            function = LambdaFunction.create(_lambda)
            functions.append(function.toDict())

        if 'NextToken' in lambdaFunction:
            LambdaFunction.token =  lambdaFunction['NextToken']
        else:
            LambdaFunction.token = None

        return functions

    @staticmethod
    def updateMemory(name, memory=None):
        cmd = ('aws lambda update-function-configuration  --function-name %s ' %name )
        if not name is None:
            cmd += (' --memory-size %s ' %memory)

        cmdOutput = os.popen(cmd).read()
        _lambda = json.loads(cmdOutput)
        function = LambdaFunction.create(_lambda)
    
        return function

    @staticmethod
    def update(name, layers=None, role=None):
        cmd = ('aws lambda update-function-configuration --function-name %s' %name)

        if isinstance(layers, list):
            layers = ' '.join(layers)

        if not layers is None:
            cmd += (' --layers %s ' %layers)

        if not role is None:
            cmd += (' --role %s ' % role)

        cmdOutput = os.popen(cmd).read()
        _lambda = json.loads(cmdOutput)
        function = LambdaFunction.create(_lambda)

        return function

    @staticmethod
    def output(functions, outputPath='./out'):
        
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)

        today = datetime.datetime.today().strftime("%Y%m%d")

        csvPath = outputPath + '/' + today +'-out.csv'
        headers = ['name', 'arn', 'role', 'layers', 'memorySize', 'codeSize', 'updated']
        
        fileExists = os.path.isfile(csvPath)

        with open(csvPath, 'a+') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)
            if not fileExists:
                    writer.writeheader()
            for lambdaInfo in functions:
                writer.writerow(lambdaInfo)

        return 1
