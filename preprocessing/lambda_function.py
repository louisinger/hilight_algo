import json
import sys
import preprocessing

def handler(event, context):
    website_name = event['websitename']
    if website_name == "Twitter":
        return  preprocessing.find_sentences('twitter.txt', 'english')
    else:
        return {'result':"nothing"}
