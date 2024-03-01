import boto3
import time
import urllib.request
import json

ec2 = boto3.client('ec2')
d_regions = ec2.describe_regions()
delay_time = 5
all_regions = []

# Server
instance_function = "Server"
auto_scaling_group_name = 'arcgis-server-AutoScalingGroup-1V8A7D19WFD39'
json_url = "https://www.arcgis-indoors.com/server/rest/info/healthCheck?f=pjson"  # Replace with your actual JSON URL
key_to_check = "success"
value_success = True

# Portal
instance_function = "Portal"
portals_ids = ["i-0c2c093d4ba1e3a65","i-05999c060c3b071c3"]
json_url = "https://www.arcgis-indoors.com/portal/portaladmin/healthCheck?f=pjson"  # Replace with your actual JSON URL
key_to_check = "status"
value_success = "success"

# Datastore
instance_function = "Datastore"
datastoress_ids = ["i-0c2c093d4ba1e3a65","i-05999c060c3b071c3"]
json_url = ""
key_to_check = "Datastore"
value_success = "success"

# FileStore
instance_function = "FileStore"

region = 'us-east-1'


def reboot_instance(instance_id, region, instance_function):
    ec2 = boto3.client('ec2', region_name=region)
    
    try:
        response = ec2.reboot_instances(InstanceIds=[instance_id])
        
        time.sleep(delay_time)  # Wait for delay_time seconds before checking

        while True:
            try:
                # Check for state        
                response = ec2.describe_instances(InstanceIds=[instance_id])
                if 'Reservations' in response and len(response['Reservations']) > 0:
                    instance = response['Reservations'][0]['Instances'][0]
                    state = instance['State']['Name']
                    # print(f"The value of 'state' is '{state}'")
                else:
                    status = '-'
                    # return False  # Instance not found or no status available
                
                # Check for status
                instance_status = ec2.describe_instance_status(InstanceIds=[instance_id])
                if 'InstanceStatuses' in instance_status and len(instance_status['InstanceStatuses']) > 0:
                    status = instance_status['InstanceStatuses'][0]['InstanceStatus']['Status']
                else:
                    return False  # Instance not found or no status available
                
                # print(f"The value of 'status' is '{status}'")

                # Check for Health
                if instance_function == "server":
                    gishealth = ArcGisTestHealth(json_url, key_to_check)
                else:
                    gishealth = value_success
                
                if state == 'running' and status == 'ok' and gishealth == value_success:
                    return True  
                else:
                    time.sleep(delay_time)  # Wait for 10 seconds before rechecking
            except Exception as e:
                print(f"Error checking instance status: {str(e)}")
                return False
    except Exception as e:
        print('Error', e)

def ArcGisTestHealth(json_url, key_to_check):
    try:
        # Open the URL and read the JSON data
        with urllib.request.urlopen(json_url) as response:
            data = response.read()
        
        # Parse the JSON data
        json_data = json.loads(data)
        
        # Check if the key is present and its value is True
        if key_to_check in json_data:
            return json_data[key_to_check]
        else:
            return json_data[key_to_check]
    
    except Exception as e:
        print(f"Error: {e}")

 
def lambda_handler(event, context):
    # Repeat this process for count(portals_ids) 
    try:
        for instance_id in portals_ids:
            response = reboot_instance(instance_id, region)
        return f"Instances {instance_id} are healthy and ready."
    
    except Exception as e:
        print('Error', e)
        return f"Instance {instance_id} is not healthy or ready"


    
