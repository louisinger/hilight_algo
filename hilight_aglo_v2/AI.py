import json
import basic_segmentation_twitter_v3
def handler(event, context):
  data = {
    'output': fn_test(event["pathParameters"]["website_name"])
  }
  return {'statusCode': 200,
    'body': json.dumps(data),
    'headers': {'Content-Type': 'application/json'}}

def fn_test(name):
	return 'je suis le test pour le parametre : ' + name


def launch_hilight(name):
	if (name == "Twitter"):
		return basic_segmentation_twitter_v3.find_sentences()
	else:
		return "null"

if __name__ == '__main__' :

	print(launch_hilight('Twitter'))
