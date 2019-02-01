import json
import boto3

def handler(event, context):
  data = {
    'output': launch_hilight(event["pathParameters"]["name"])
  }
  return {'statusCode': 200,
    'body': json.dumps(data),
    'headers': {'Content-Type': 'application/json'}}


def launch_hilight(name):
	return "Launch the AI for " + name
