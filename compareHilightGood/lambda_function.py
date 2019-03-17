import json
import compareHIlightGood

def lambda_handler(event, context):
    response = compareHIlightGood.getPrivacyGradesPerCriter(event['preprocessing'])
    return response
