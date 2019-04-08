import json 
import basic_plotly_v2

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
            'body': basic_plotly_v2.compare_from_api(website)  
            }
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
        
    return response

def handler2(event, context):
    response = {}
    try:
        response = {
            'statusCode': 200,
            'headers': {
                "Content-Type" : "application/json",
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Headers" : "*"
            },
            'body': basic_plotly_v2.compare_between_cgu(['twitter', 'facebook', 'amazon'])  
            }
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
        
    return response
