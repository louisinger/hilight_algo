import json

def lambda_handler(event, context):
    return "Le double de votre nombre est:  " + event['number']*2
