import json 
import boto3

lambda_client = boto3.client('lambda')

def handler(event, context):
    payload_preprocessing = {}
    payload_preprocessing['websitename'] = event['path']['websitename']

    payload_compare = {}
    
    response = {}

    try:
        preprocessing_result = lambda_client.invoke(
        FunctionName='preprocessing-dev-preprocessing',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload_preprocessing)
        )
        preprocessing_res = json.loads(preprocessing_result['Payload'].read())

        payload_compare['preprocessing'] = preprocessing_res
        
        compare_result = lambda_client.invoke(
            FunctionName='compare-hilight-good-dev-compare',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload_compare)
        )
        
        body_res = json.loads(compare_result['Payload'].read())
        response = {
            'statusCode': 200,
            'headers': {
                "Content-Type" : "application/json",
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Headers" : "*"
            },
            'body': json.dumps(body_res)  
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
     
