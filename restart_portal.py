import boto3
import time
# 63924.39 ms per restart

ec2 = boto3.client('ec2')
d_regions = ec2.describe_regions()
delay_time = 10
all_regions = []

region = 'us-east-1'


def start_instance(instance_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
    
    except Exception as e:
        if 'DryRunOperation' not in str(e):
            raise
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        while True:
            try:
                # Check for state            
                response = ec2.describe_instances(InstanceIds=[instance_id])
                
                if 'Reservations' in response and len(response['Reservations']) > 0:
                    instance = response['Reservations'][0]['Instances'][0]
                    state = instance['State']['Name']
                else:
                    #print("32- Couldn't check the state\n")
                    return False  # Instance not found or no status available
                
                # Check for status
                instance_status = ec2.describe_instance_status(InstanceIds=[instance_id])
                if 'InstanceStatuses' in instance_status and len(instance_status['InstanceStatuses']) > 0:
                    status = instance_status['InstanceStatuses'][0]['InstanceStatus']['Status']
                else:                        
                    #print("40- Couldn't check the status\n")
                    status = '-'
                    #return False  # Instance not found or no status available
                
                # Check for Health
                if state == 'running' and status == 'ok':
                    print( f"Instance {instance_id} is healthy and ready")
                    return True  # Instance is Running and ready to start
                else:
                    #print("47- Wait for 10 seconds before rechecking\n")                    
                    time.sleep(10)  # Wait for 10 seconds before rechecking
            except Exception as e:
                print(f"Error checking instance status: {str(e)}")
                return False
        
        #print('Starting Success', response)
   
    except Exception as e:
        print('Error', e)

def stop_instance(instance_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except Exception as e:
        if 'DryRunOperation' not in str(e):
            raise
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print('Success', response)

    except Exception as e:
        print('Error', e)


def reboot_instance(instance_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    try:
        ec2.reboot_instances(InstanceIds=[instance_id], DryRun=True)
    except Exception as e:
        if 'DryRunOperation' not in str(e):
            print('You do not have permission to reboot')
            raise
    try:
        response = ec2.reboot_instances(InstanceIds=[instance_id], DryRun=False)
        print('Success', response)
    except Exception as e:
        print('Error', e)

def wait_until_stopped(instance_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    while True:
        try:
            response = ec2.describe_instances(InstanceIds=[instance_id])
            if 'Reservations' in response and len(response['Reservations']) > 0:
                instance = response['Reservations'][0]['Instances'][0]
                state = instance['State']['Name']
            else:
                return False  # Instance not found or no status available
            
            if state == 'stopped': 
                return True  # Instance is stopped and ready to start
            else:
                time.sleep(10)  # Wait for 10 seconds before rechecking
        except Exception as e:
            print(f"(wait_until_stopped)Error checking instance status: {str(e)}")
            return False


def check_instance_health(instance_id, region):
    ec2 = boto3.client('ec2', region)
    while True:
        try:
            # Check for state            
            response = ec2.describe_instances(InstanceIds=[instance_id])
            if 'Reservations' in response and len(response['Reservations']) > 0:
                instance = response['Reservations'][0]['Instances'][0]
                state = instance['State']['Name']
            else:
                status = '-'
                # return False  # Instance not found or no status available
            
            # Check for status
            instance_status = ec2.describe_instance_status(InstanceIds=[instance_id])
            if 'InstanceStatuses' in instance_status and len(instance_status['InstanceStatuses']) > 0:
                status = instance_status['InstanceStatuses'][0]['InstanceStatus']['Status']
            else:
                return False  # Instance not found or no status available
            
            # Check for Health
            if state == 'running' and status == 'ok':
                return True  # Instance is Running and ready to start
            else:
                time.sleep(10)  # Wait for 10 seconds before rechecking
        except Exception as e:
            print(f"Error checking instance status: {str(e)}")
            return False



def Restart(instance_id, region):
    
    # RESTARTING
    #Stopping Instance
    print('Stopping instance\n')
    stop_instance(instance_id, region)
    # Wait for instance to be stopped
    if wait_until_stopped(instance_id, region):
        print('Starting instance\n')
        start_instance(instance_id, region)
    else:
        return {
            'statusCode': 500,
            'body': f"Instance {instance_id} is not stopped or not available"
        }


def lambda_handler(event, context):
    Restart('i-0735087dd5adc1c0a', region) #     instance_id = 'i-0735087dd5adc1c0a' # portal 1
    #time.sleep(delay_time)  # Wait for delay_time seconds before next step






