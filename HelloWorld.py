import json

def lambda_handler(event, context):
    print("request", json.dumps(event))
    i=0
    while i<event['count']:
        print(event['message'])
        i+=1
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
