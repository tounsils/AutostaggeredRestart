import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    instance_id = 'i-0735087dd5adc1c0a'  # Replace with your EC2 instance ID

    # Restart the instance
    try:
        ec2.reboot_instances(InstanceIds=[instance_id])
        print(f"Restarting instance {instance_id}...")
        return {
            'statusCode': 200,
            'body': f"Restarting instance {instance_id}..."
        }
    except Exception as e:
        print(f"Failed to restart instance {instance_id}: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Failed to restart instance {instance_id}: {str(e)}"
        }


'''
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