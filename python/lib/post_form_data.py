import requests
from urllib3 import encode_multipart_formdata
import json

''' 
postnman form-data post
'''

def post_form_data(url, payload, header={}):
    encode_payload = encode_multipart_formdata(payload)
    form_data = encode_payload[0]
    header['Content-Type'] = encode_payload[1]
    r = requests.post(url, headers=header, data=form_data)
    res = r.content.decode('utf-8')
    return json.loads(res)


url = "" 
payload = {'key':"value"}
r = post_form_data(url, payload)

