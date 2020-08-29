
import boto3

''' SET aws_access_key_id & aws_secret_access_key in code '''
s3 = boto3.resource('s3', 
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)

''' Get obj and put in AWS lambda Function'''
def getSpecificObjPutTmp(specificObjName, bucketName):
    s3 = boto3.resource('s3')
    mybucket = s3.Bucket(bucketName)
    lambdaTmpPath = '/tmp/'
    for obj in mybucket.objects.all():
        if specificObjName in obj.key:
            # obj.key is obj' name
            fileName = obj.key
            size = obj.size # size
            keyPath = lambdaTmpPath + fileName
            mybucket.download_file(fileName, keyPath)
            return keyPath
    return None

''' Upload a file (diff from object) to S3 from AWS lambda Fuction'''
def uploadFile(filePath='/text.txt', bucketName):
    s3 = boto3.resource('s3')
    mybucket = s3.Bucket(bucketName)
    lambdaTmpPath = '/tmp/'
    s3FolderPath = '/'
    fileName = 'text.txt'
    mpixBucket.upload_file('/tmp/'+filePath, s3FolderPath + fileName)
    return None


''' Get Specific Obj Use Filter '''
def getSpecificObj(spcificPath, bucketName):
    s3 = boto3.resource('s3')
    mybucket = s3.Bucket(bucketName)
    for obj in mybucket.objects.filter(spcificPath):
        fileName = obj.key
        size = obj.size # size
    return None

''' Copy a file from a folder to another folder '''
def copyObjtoAnotherFolder(bucketName, sourcePath, newPath):
    # sourcePath = '/myfolder_one/file.txt'
    # newPath = '/myfolder_two/file.txt'
    s3 = boto3.resource('s3')
    copy_source = {
        'Bucket': bucketName, # or the other bucket.
        'Key': sourcePath
    }
    extra_args = {'ACL': 'public-read'}
    bucket = s3.Bucket(bucketName)
    bucket.copy(copy_source, newPath, extra_args)
    return 1


''' Put an file to Bucket'''
def putObj(bucketName, folder, fileName, obj):
    s3 = boto3.resource('s3')
    mybucket = s3.Bucket(bucketName)
    obj = open(('./want_to_upload_obj_file_path.txt'), 'rb')
    
    if folder[-1] != '/':
        filePath = folder +'/'+fileName
    else:
        filePath = folder +'/'+fileName
    mybucket.put_object(Key=filePath, Body=obj)
    return 1

''' Delete specific obj (or dir) from Bucket '''
def deleteObj(bucketName, folder, fileName, obj):
    s3 = boto3.resource('s3')
    mybucket = s3.Bucket(bucketName)
    if folder[-1] != '/':
        filePath = folder +'/'+fileName
    else:
        filePath = folder +'/'+fileName
    mybucket.objects.filter(Prefix=filePath).delete()


''' Show specific obj summary '''
def summaryObj(bucketName, folder, fileName, obj):
    s3 = boto3.resource('s3')
    if folder[-1] != '/':
        filePath = folder +'/'+fileName
    else:
        filePath = folder +'/'+fileName
    summary = s3.ObjectSummary(bucketName, filePath)
    '''
    summary available attributes:
    - e_tag
    - last_modified
    - owner
    - size
    - storage_class 
    '''
    return summary.size

''' List top-level common prefixes in Amazon S3 bucket '''
def getTopFolderNameList(bucketName):
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects')
    result = paginator.paginate(Bucket=bucketName, Delimiter='/')
    slugList = [ prefix.get('Prefix').replace('/', '') for prefix in result.search('CommonPrefixes')]
    
    return slugList

