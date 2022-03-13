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
Requires the following Environment Variables:
- discord_webhook_url
    The webhook url for the 'minecraft' Discord channel.

The event value 'queryStringParameters' is retrieved from API Gateway.

Timeout needs to be increased to allow the loop to run.
Sometimes EC2 instances can take a few minutes to spin up.
"""
def lambda_handler(event, context):
    region = "eu-west-2"
    instance_id = event["queryStringParameters"]['instanceId']
    discord_webhook_url = os.environ["discord_webhook_url"]
    
    ec2_resource = boto3.resource('ec2', region_name=region)

    try:
        instance = ec2_resource.Instance(instance_id)
        instance.start()
        while instance.state['Name'] != 'running':
            print(f"...instance is {instance.state['Name']}")
            time.sleep(10)
            instance.load()

        instance_ip = instance.public_ip_address
        if not instance_ip:
            raise ValueError('Server IP address was empty')

        discord_content = f"The Vanilla Minecraft server: **{get_tag_from_instance(instance, 'Name')}** has been started.\nIP address - *{instance_ip}*."
        webhook = DiscordWebhook(url=discord_webhook_url, content=discord_content)
        webhook.execute()

        return {
            'statusCode': 200,
            'body': json.dumps({'running': True}),
            'headers': {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : True
            }
        }
    except Exception as e:
        print('Failed to start instance ' + instance_id)
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'unable to start server'}),
            'headers': {
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Credentials" : True
            }
        }
