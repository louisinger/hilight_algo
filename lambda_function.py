import json
import sys
sys.path.append(r"./hilight_aglo_v2")
sys.path.append(r"./package")
sys.path.append(r"./hilight_aglo_v2/rateScripts")

#import preprocessing
import compareHIlightGood
import preprocessing

if __name__== "__main__":
    #preprocessing.find_sentences('twitter.txt', 'english')
    json = preprocessing.find_sentences('twitter.txt', 'english')
    compareHIlightGood.getPrivacyGradesPerCriter(json)

def lambda_handler(event, context):
    website_name = "Twitter"
    if website_name == "Twitter":
        return  preprocessing.find_sentences('twitter.txt', 'english')

def all_process(event, context):
    ''' To run preprocess + vectortest + visualisation
    '''
    json = preprocessing.find_sentences('twitter.txt', 'english')
    compareHIlightGood.getPrivacyGradesPerCriter(json)