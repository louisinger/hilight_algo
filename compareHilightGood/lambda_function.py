import json
import compareHIlightGood

def handler(event, context):
    preprocessingResult = event['preprocessing']
    if(preprocessingResult != null){
        response = compareHIlightGood.getPrivacyGradesPerCriter(event['preprocessing'])
    } else {
        response = '{"msg": "no preprocssing in the event"}'
    return response
