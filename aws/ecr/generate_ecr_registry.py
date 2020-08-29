import os
ACCOUNT = '322570661063'
REGION = 'ap-southeast-1'
SECRET_NAME = REGION+'-ecr-registry'
EMAIL = 'y02121148s@gmail.com'

TOKEN = 'aws ecr --region=$REGION get-authorization-token \
        --output text \
        --query authorizationData[].authorizationToken | base64 -d | cut -d: -f2'

#  Create or replace registry secret
cmds = [
 'kubectl delete secret --ignore-not-found {SECRET_NAME}'.format(SECRET_NAME=SECRET_NAME),
 'kubectl create secret docker-registry {SECRET_NAME} \
 --docker-server=https://{ACCOUNT}.dkr.ecr.{REGION}.amazonaws.com \
 --docker-username=AWS \
 --docker-password="{TOKEN}" \
 --docker-email="{EMAIL}"'.format(SECRET_NAME=SECRET_NAME, ACCOUNT=ACCOUNT, REGION=REGION, TOKEN=TOKEN, EMAIL=EMAIL)
]

for cmd in cmds:
    stream = os.popen(cmd)
    output = stream.read()
    print(output)