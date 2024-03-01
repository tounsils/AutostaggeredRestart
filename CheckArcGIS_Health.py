import boto3
import urllib.request
import json

# https://www.afrsmapping360.com/server/rest/info/healthCheck?f=pjson
# {"success": true}

def check_value_in_json(url, key_to_check):
    try:
        # Open the URL and read the JSON data
        with urllib.request.urlopen(url) as response:
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
    json_url = "https://www.afrsmapping360.com/server/rest/info/healthCheck?f=pjson"  # Replace with your actual JSON URL
    key_to_check = "success"  # Replace with the key you want to check
    
    print(f"The value of '{key_to_check}' is '{check_value_in_json(json_url, key_to_check)}'")




