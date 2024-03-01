import boto3

def lambda_handler(event, context):
    # Initialize the AWS Auto Scaling client
    autoscaling_client = boto3.client('autoscaling')
    
    # Get the name of your Auto Scaling group
    auto_scaling_group_name = 'arcgis-server-AutoScalingGroup-1V8A7D19WFD39'
    
    # Retrieve instances in the Auto Scaling group
    response = autoscaling_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[auto_scaling_group_name]
    )
    
    # Extract instance details
    instances = []
    for group in response['AutoScalingGroups']:
        for instance in group['Instances']:
            instances.append(instance['InstanceId'])
    
    # Print or process instance details
    print("Instances in Auto Scaling group:", instances)
    
    # Return any necessary output
    return {
        'statusCode': 200,
        'body': instances
    }
