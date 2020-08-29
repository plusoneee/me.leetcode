# Created a script that pulls the token from AWS-ECR
ACCOUNT=AWS_ACCOUNT
REGION=AWS_REGION
SECRET_NAME=${REGION}-ecr-registry
EMAIL=email@email.com

TOKEN=`aws ecr --region=$REGION get-authorization-token --output text --query authorizationData[].authorizationToken | base64 -d | cut -d: -f2`

kubectl delete secret --ignore-not-found $SECRET_NAME
kubectl create secret docker-registry $SECRET_NAME \
 --docker-server=https://${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com \
 --docker-username=AWS \
 --docker-password="${TOKEN}" \
 --docker-email="${EMAIL}"