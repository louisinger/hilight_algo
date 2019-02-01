import json
import sys
sys.path.append(r"./hilight_aglo_v2")
sys.path.append(r"./package")

import basic_segmentation_twitter_v3

def lambda_handler(event, context):
    website_name = "Twitter"
    if website_name == "Twitter": 
        return  basic_segmentation_twitter_v3.find_sentences('twitter.txt', 'english')
    
	

    
