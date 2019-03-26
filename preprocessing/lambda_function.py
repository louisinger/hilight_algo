import json
import sys
import preprocessing
import boto3

'''
function permettant de recuperer le text d'une CGU en fonction d'un nom de site.
Utilise boto3 pour generer un client dynamoDB et acceder à la database d'Hilight.

param:
    key:
        type: String
        comment: nom de site (clé primaire dans la DB)
'''
def get_text(key):
    result = ''
    try:
        dynamoDB = boto3.resource('dynamodb')
        table = dynamoDB.Table('CGU')
        response = table.get_item(
            Key={'domain':key.lower()}
         )
        result = response['Item']['content']
    except Exception as e:
        result = 'error'
        raise e

    return result

'''
handler de la fonction lambda sur AWS. 
'''
def handler(event, context):
    response = {}

    try:
        website_name = event['websitename']
        text = get_text(website_name)
        if text == 'error':
            response['statue'] = 'error'
        else:
            response['result'] = preprocessing.find_sentences(text, 'english')
            response['statue'] = 'success'
    except Exception as e:
        response['statue'] = 'error'
        response['result'] = e
    
    return json.dumps(response)
