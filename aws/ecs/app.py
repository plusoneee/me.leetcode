
import boto3
import json


def getTaskCountNumber(cluster=[]):
    client = boto3.client('ecs')
    
    response = client.describe_clusters(clusters=cluster)
    clusterDict = response['clusters'][0]
    
    runningTasksCount = int(clusterDict['runningTasksCount'])
    pendingTasksCount = int(clusterDict['pendingTasksCount'])

    return (runningTasksCount, pendingTasksCount)

getTaskCountNumber(['my_cluster_name'])


def runClusterServiceTask(cluster, taskDefinition, subnets, securityGroups, launchType='FARGATE', platformVersion='LATEST'):
    client = boto3.client('ecs')
    response = client.run_task(
        cluster = cluster,
        launchType = launchType,
        taskDefinition = taskDefinition,
        count = 1,
        platformVersion=platformVersion,
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': subnets,
                'securityGroups': securityGroups,
                'assignPublicIp': 'ENABLED'
            }
        })
    
    tasks = response['tasks']
    for task in tasks:
        task['createdAt'] = str(task['createdAt'])
    
    return json.dumps(tasks)

taskDefinition='first-run-task-definition:1' # task definition
cluster='my_cluster_name' # ECS Cluster Mame 

# See Service: my_cluster_name-servuce Network Access
subnets = ['my_subnet_name']
securityGroups = ["my_security_group1"]

# run task
runClusterServiceTask(cluster, taskDefinition, subnets, securityGroups, launchType='FARGATE', platformVersion='LATEST')
