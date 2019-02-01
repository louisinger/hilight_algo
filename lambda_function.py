import json
import sys
sys.path.append(r"./hilight_aglo_v2")
sys.path.append(r"./package")

import prepocessing.py

def lambda_handler(event, context):
    website_name = "Twitter"
    if website_name == "Twitter":
        return  preprocessing.find_sentences('twitter.txt', 'english')
