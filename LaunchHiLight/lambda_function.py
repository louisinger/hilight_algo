import json 
import boto3

lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    payload_preprocessing = {}
    payload_preprocessing['websitename'] = event['number']

    payload_compare = {}
    try:
        preprocessing_result = lambda_client.invoke(
            FunctionName='preprocessing',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload_preprocessing)
        )

        payload_compare['preprocessing'] = preprocessing_result

        response = lambda_client.invoke(
            FunctionName='compareHilightGood',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload_compare)
        )

        return response
    except Exception as e:
        print(e)
        raise e

