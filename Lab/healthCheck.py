import boto3
import time

def check_instance_health(instance_id):
    ec2 = boto3.client('ec2')
    while True:
        try:
            instance_status = ec2.describe_instance_status(InstanceIds=[instance_id])
            if not instance_status['InstanceStatuses']:
                return False  # Instance not found or no status available

            state = instance_status['InstanceStatuses'][0]['InstanceState']['Name']
            status = instance_status['InstanceStatuses'][0]['InstanceStatus']['Status']
            
            if state == 'running' and status == 'ok':
                return True  # Instance is running and healthy

            time.sleep(10)  # Wait for 10 seconds before rechecking
        except Exception as e:
            print(f"Error checking instance status: {str(e)}")
            return False

def lambda_handler(event, context):
    instance_id = 'YOUR_INSTANCE_ID'  # Replace with your EC2 instance ID
    
    # Check instance health and wait until ready
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
