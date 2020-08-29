import hashlib
from urllib.parse import parse_qs
import datetime

class NewebPayHash():
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def generateCheckValue(self, queryParameter):
        sortedQueryParameter = NewebPayHash.sortQueryParameter(queryParameter)
        queryParameter = 'IV={iv}&{qP}&Key={key}'.format(iv=self.iv, key=self.key, qP=sortedQueryParameter)
        hashCheckValue = NewebPayHash.hashQueryParameterStr(queryParameter)
        return hashCheckValue

    def generateCheckCode(self, queryParameter):
        sortedQueryParameter = NewebPayHash.sortQueryParameter(queryParameter)
        queryParameter = 'HashIV={iv}&{qP}&HashKey={key}'.format(iv=self.iv, key=self.key, qP=sortedQueryParameter)
        hashCheckCode = NewebPayHash.hashQueryParameterStr(queryParameter)
        return hashCheckCode

    @staticmethod
    def hashQueryParameterStr(queryParameter):
        m = hashlib.sha256()
        m.update(queryParameter.encode('utf-8'))
        return m.hexdigest().upper()

    @staticmethod
    def sortQueryParameterWithDict(dictItem):
        queryParameterSorted = ''
        for key in sorted(dictItem.keys()):
            if isinstance(dictItem[key], list):
                value = dictItem[key][0]
            else:
                value = str(dictItem[key])
            queryParameterSorted += key+'='+value +'&'
        return queryParameterSorted[:-1] # [:-1] to remove ending '&'.
        

if __name__ == '__main__':
    
    # test
    np = NewebPayHash(key="abcdefg", iv="1234567")
    dictItem = {
        "Amt":"100",
        "MerchantID":"1422967",
        "MerchantOrderNo":"840f022",
        "TradeNo":"14061313541640927"
    }
    queryParameter = NewebPayHash.sortQueryParameterWithDict(dictItem)
    checkValue = np.generateCheckValue(queryParameter)
