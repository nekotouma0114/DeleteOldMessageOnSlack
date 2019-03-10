import boto3
import json

class DynamoDB:
    dynamodb = None
    def __init__(self,access_key,secretkey,resion="ap-northeast-1"):
        session = boto3.Session(aws_access_key_id=accesskey, aws_secret_access_key=secretkey, region_name=region)
        self.dynamodb = session.resource('dynamodb')

    def scan(self,table_name):
        table = self.dynamodb.Table(table_name)
        data = table.scan()
        #TODO: check http code and cehck exception
        return data['Items']
