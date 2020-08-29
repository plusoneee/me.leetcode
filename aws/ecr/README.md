### Install Docker and AWS CLI
- Docker version >= 1.7

### Authentication to AWS
- Access key and Srcret key could be found from the IAM on AWS.
```bash
> aws configure
```

### Login to AWS ECR
- `get-login` command to log in to AWS elastic container registry. 
```bash
> aws ecr get-login --region {aws-region-name} > login-info.txt
```
- Get `login-info.txt` which contain the command for login, could just paste it on terminal(cmd):
```bash
docker login -u AWS -p {password} https://{your_aws_account_id}.dkr.ecr.{aws-region-name}.amazonaws.com
```

### Download the Ubuntu Image
- Download any (docker)image in your local. For exmaple:
```bash
docker pull ubuntu:16.04
```

### Create a Repository on ECR
- Could create a repository from [Amazon ECR Management Console](https://aws.amazon.com/tw/ecr/) or command:
```bash
> aws ecr create-repository --repository-name {repository-name}

{
    "repository": {
        "repositoryArn": "arn:aws:ecr:{aws-region-name}:{your_aws_account_id}:repository/{repository-name}",
        "registryId": "{your_aws_account_id}",
        "repositoryName": "{repository-name}",
        "repositoryUri": "{your_aws_account_id}.dkr.ecr.{aws-region-name}.amazonaws.com/{repository-name}",
        "createdAt": 1576819683.0,
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        }
    }
}

```

### Tag Image
```bash
docker tag {my_image_name}:{tag} {your_aws_account_id}.dkr.ecr.{aws-region-name}.amazonaws.com/{repository_name}
```
- (optional) Verify the image has been tagged `docker images`.

### Push the Image into Amazon ECR
Use `push` command to move the ubuntu image into ECR:
```bash
docker push {your_aws_account_id}.dkr.ecr.{aws-region-name}.amazonaws.com/{repository_name}
```

### Delete Image from Repository
```bash
aws ecr batch-delete-image --repository-name {repository-name} --image-ids imageTag=16.04
```

### Delete Repository
```bash
aws ecr delete-repository --repository-name {repository-name}
```
