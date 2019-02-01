import json
import sys
sys.path.append(r"./hilight_aglo_v2")
sys.path.append(r"./package")

import preprocessing
if __name__== "__main__":
    preprocessing.find_sentences('twitter.txt', 'english')

def lambda_handler(event, context):
    website_name = "Twitter"
    if website_name == "Twitter":
        return  preprocessing.find_sentences('twitter.txt', 'english')
