from Crypto.Cipher import AES
import base64
from binascii import b2a_hex, a2b_hex

# AES-256
class AESCrypt():
    def __init__(self, key, iv, code=None):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = iv.encode('utf-8')
        self.code = code

    def encrypt(self, text, blockSize=32):
        text = text
        cryptor = AES.new(self.key, self.mode, self.iv)
        count = len(text)
        
        if count < blockSize:
            add = (blockSize - count)
            self.code = chr(add)
            text = text + (self.code * add) 
            
        elif count > blockSize:
            add = blockSize - (count % blockSize)
            self.code = chr(add)
            # return str(type(text))
            text = text + (self.code * add) 
        
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip(self.code)

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
    pc = AESCrypt(key='12345678901234567890123456789012', iv='1234567890123456') 
    e = pc.encrypt("PLUSONEPLUSONE")
    d = pc.decrypt("77f377b85274595fd04a1586f5590b7dc4ecfff60d2997069077f6b47053ffcf")
