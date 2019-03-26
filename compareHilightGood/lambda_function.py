import json
import compareHIlightGood
import traceback

def handler(event, context):
    try:
        preprocessingResult = event['preprocessing']
        response = json.dumps(compareHIlightGood.getPrivacyGradesPerCriter(json.loads(preprocessingResult)))
    except Exception as e:
        response = 'error: '+ str(e) + '\n'
        response += 'stackTrace: ' + traceback.format_exc()
        response += 'json: ' + preprocessingResult
    return response
