import boto3

def lambda_handler(event, context):
    instance_function = "Server"
    auto_scaling_group_name = 'arcgis-server-AutoScalingGroup-1V8A7D19WFD39'
    json_url = "https://www.arcgis-indoors.com/server/rest/info/healthCheck?f=pjson"  # Replace with your actual JSON URL
    key_to_check = "success"
    value_success = True
    # Initialize the AWS Auto Scaling client
    autoscaling_client = boto3.client('autoscaling')
    # Get the name of your Auto Scaling group
    # auto_scaling_group_name = 'arcgis-server-AutoScalingGroup-1V8A7D19WFD39'
    # Retrieve instances in the Auto Scaling group
    response = autoscaling_client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[auto_scaling_group_name]
    )
    server_instances = []
    for group in response['AutoScalingGroups']:
        for instance in group['Instances']:
            server_instances.append(instance['InstanceId'])
    
    # Print or process instance details
    print("Instances in Auto Scaling group:", server_instances)
    
    # Return any necessary output
    return {
        'statusCode': 200,
        'body': server_instances
    }
