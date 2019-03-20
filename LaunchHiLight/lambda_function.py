import json 
import boto3

lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    payload_preprocessing = {}
    payload_preprocessing['websitename'] = event['queryStringParameters']['websitename']

    payload_compare = {}
    
    response = {}
    
    try:
        
        preprocessing_result = lambda_client.invoke(
            FunctionName='preprocessing',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload_preprocessing)
        )
        '''
        payload_compare['preprocessing'] = preprocessing_result

        compare_result = lambda_client.invoke(
            FunctionName='compareHilightGood',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload_compare)
        )
        '''
        
        response = {
            'statusCode': 200,
            'headers': {
                "Content-Type" : "application/json",
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Headers" : "*"
            },
            'body': preprocessing_result
        }

        return response
    except Exception as e:
        response = {
            'statusCode': 500,
            'headers': {
                "Content-Type" : "application/json",
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Headers" : "*"
            },
            'body': 'Erreur coté serveur - HiLight'
        }
        print(e)
        raise e

