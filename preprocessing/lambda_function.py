import json
import sys
#import preprocessing
import preprocessing

def lambda_handler(event, context):
    website_name = event['websitename']
    if website_name == "Twitter":
        return  preprocessing.find_sentences('twitter.txt', 'english')
