import boto3
import json

def lambda_handler(event, context):
    ec2 = boto3.client("ec2")
    #status = ec2.describe_instance_status(IncludeAllInstances=True)
    
    instance_id = 'i-0735087dd5adc1c0a'  # Replace with your EC2 instance ID
    
    status = ec2.describe_instance_status(InstanceIds=[instance_id])
    
    
    
    for i in status["InstanceStatuses"]:
        instanceId = i["InstanceId"]
        InstanceState = i["InstanceState"]['Name']   # This is the line
        status = i["InstanceStatus"]["Status"]
        print(f"Instance ID: {instanceId}, State: {InstanceState}, Status: {status}")


'''

WE WORKING ON i["InstanceState"]['Name'] = State
"body": "Failed to perform action on instance i-0735087dd5adc1c0a: 'InstanceState'"

Test Event Name
testing

Response
null

Function Logs
START RequestId: 1b02514a-6307-4304-8b92-76f849b695bf Version: $LATEST
i-0735087dd5adc1c0a :  not-applicable
Instance ID: i-0735087dd5adc1c0a, State: stopped, Status: not-applicable
END RequestId: 1b02514a-6307-4304-8b92-76f849b695bf
REPORT RequestId: 1b02514a-6307-4304-8b92-76f849b695bf	Duration: 2547.91 ms	Billed Duration: 2548 ms	Memory Size: 128 MB	Max Memory Used: 88 MB	Init Duration: 299.85 ms

Request ID
1b02514a-6307-4304-8b92-76f849b695bf
'''
