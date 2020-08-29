import json
from urllib.parse import parse_qs, urlencode

class QueryParameterConvert():
    
    def __init__(self, postData):
        self.postData = postData
        self.qParameterDict = None

    def toDict(self):
        if not self.qParameterDict is None:
            return self.qParameterDict

        queryParameterDict = parse_qs(self.postData)
        for key in queryParameterDict.keys():
            value = queryParameterDict[key]
            if isinstance(value, list) and len(value)==1:
                queryParameterDict[key] = value[0]

        self.qParameterDict = queryParameterDict
        return self.qParameterDict


if __name__ == '__main__':
    qpc  = QueryParameterConvert("RespondType=Json&TimeStamp=1400137200&IndexType=1&CloseType=1")
    print(qpc.toDict())
   