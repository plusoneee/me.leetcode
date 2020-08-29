## AWC CLI
* Install
```
pip install awscli
```
* Downloading an entire S3 bucket.
```
aws s3 sync s3://<source_bucket> <local_destination>
```
* For example:
```
aws s3 sync s3://mybucketname/foldername .
```
