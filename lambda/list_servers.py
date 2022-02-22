import json
import boto3


def get_server_name(instance):
    for tag in instance.tags:
        if tag['Key'] == 'Name':
            return tag['Value']


def get_minecraft_type(instance):
    for tag in instance.tags:
        if tag['Key'] == 'minecraft_type':
            return tag['Value']


def lambda_handler(event, context):
  print('received event:')
  print(event)

  instances = {
      "running": [],
      "stopped": []
  }
  region = "eu-west-2"  
  
  filter = [{
    'Name':'tag:minecraft',
    'Values': ['']}]

  try:
    ec2_resource = boto3.resource('ec2', region_name=region)

    response = ec2_resource.instances.filter(Filters=filter)

    for i in response:
        instance = {
            "serverName": get_server_name(i),
            "serverType": get_minecraft_type(i),
            "minecraftVersion": "",
            "availabilityZone": region,
            "instanceState": i.state["Name"]
        }

        if i.state["Name"] == "running":
            instances['running'].append(instance)
        else :
            instances['stopped'].append(instance)

  except Exception as e:
      print(f"Error retrieving servers, Error: {e.message}")

  return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST,GET'
      },
      'body': json.dumps(instances)
  }