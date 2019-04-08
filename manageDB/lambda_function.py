import json
import boto3
import update_database

def handler(event, context):
	dynamodb = boto3.client('dynamodb')
	cgus = update_database.main_function() 
	for cgu in cgus:
		dynamodb.put_item(TableName='CGU', Item = {
			'domain':{"S": cgu[0]},
			'content': {"S": cgu[1]}
			})
	return True
