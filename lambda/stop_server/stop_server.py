from discord_webhook import DiscordWebhook
import os
import json
import boto3
import time

def get_tag_from_instance(instance, key: str):
    for tag in instance.tags:
        if tag['Key'] == key:
            return tag['Value']

"""
stop_server

Requires the following python layers:
- discord_layer
    Contains the discord_webhook lib and its dependencies.

Requires the following Environment Variables:
- discord_webhook_url
    The webhook url for the 'minecraft' Discord channel.

The event value 'queryStringParameters' is retrieved from API Gateway.

Timeout needs to be increased to allow the loop to run as sometimes 
instances can take a few minutes to shut down.
"""
def lambda_handler(event, context):
	region = "eu-west-2"
	instance_id = event["queryStringParameters"]['instanceId']
	discord_webhook_url = os.environ["discord_webhook_url"]

	ec2_resource = boto3.resource('ec2', region_name=region)

	try:
		instance = ec2_resource.Instance(instance_id)
		
		if instance.state['Name'] == 'stopped':
			raise Exception('Server already stopped')

		instance.stop()
		while instance.state['Name'] != 'stopped':
			print(f"...instance is {instance.state['Name']}")
			time.sleep(10)
			instance.load()	

		discord_content = f"The Minecraft server: **{get_tag_from_instance(instance, 'Name')}** has been stopped."
		webhook = DiscordWebhook(url=discord_webhook_url, content=discord_content)
		webhook.execute()

		return {
			'statusCode': 200,
			'body': json.dumps({'running': False}),
			'headers': {
				'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
			}
		}
	except Exception as e:
		print('Failed to stop instance ' + instance_id)
		print(e)
		return {
            'statusCode': 500,
            'body': json.dumps({'error': 'unable to stop server'}),
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            }
        }
