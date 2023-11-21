#    instance_id = 'i-0735087dd5adc1c0a'  # Replace with your EC2 instance ID
import boto3
import time

region = 'us-east-1'
instance_id = 'i-0735087dd5adc1c0a'
ec2 = boto3.client('ec2', region_name=region)

def check_instance_health(instanceId):
    ec2 = boto3.client('ec2')
    while True:
        try:
            instance_status = ec2.describe_instance_status(InstanceIds=[instanceId])
            if not instance_status['InstanceStatuses']:
                return False  # Instance not found or no status available

            state = instance_status['InstanceStatuses'][0]['InstanceState']['Name']
            status = instance_status['InstanceStatuses'][0]['InstanceStatus']['Status']
            
            if state == 'running' and status == 'ok':
                return True  # Instance is running and healthy

            time.sleep(10)  # Wait for 10 seconds before rechecking
        except Exception as e:
            print(f"(check_instance_health) Error checking instance status: {str(e)}")
            return False


def lambda_handler(event, context):
    #STOPPIONG
    ec2.stop_instances(InstanceIds=[instance_id])
    print('stoped your instances: ' + instance_id)

    #CHECKING
    if check_instance_health(instance_id):
        return {
            'statusCode': 200,
            'body': f"Instance {instance_id} is healthy and ready"

        }
    else:
        return {
            'statusCode': 500,
            'body': f"Instance {instance_id} is not healthy or ready"
        }

    #STARTING
    ec2.start_instances(InstanceIds=[instance_id])
    print('started your instances: ' + instance_id)

    #CHECKING
    if check_instance_health(instance_id):
        return {
            'statusCode': 200,
            'body': f"Instance {instance_id} is healthy and ready"

        }
    else:
        return {
            'statusCode': 500,
            'body': f"Instance {instance_id} is not healthy or ready"
        }




