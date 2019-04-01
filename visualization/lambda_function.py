import json 
import basic_plotly_v2.py

def handler(event, context):
    response = {}
    try:
	website = event['path']['websitename']	

        response = {
            'statusCode': 200,
            'headers': {
                "Content-Type" : "application/json",
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Headers" : "*"
            },
            'body':   
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
     
