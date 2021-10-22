"""
Example of using moto to mock out DynamoDB table
"""

import boto3
from moto import mock_dynamodb2
import store

import pytest

from daily_vaccine_total_by_state import app

@mock_dynamodb2
def test_write_into_table():
	"Test the write_into_table with a valid input data"
	dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
	table_name = 'test'
	table = dynamodb.create_table(TableName = table_name,
								KeySchema = [
								{'AttributeName': 'MeasureName', 'KeyType': 'HASH'}],
								AttributeDefinitions = [
								{'AttributeName': 'MeasureName', 'AttributeType': 'S'}])
	data = {'MeasureName': 'NT - Administration state - Daily increase doses recorded',
			'Total': 123456}
	#store.write(data, table_name)
	table.put_item(Item=data)
	#response = table.get_item(Key={'MeasureName': data['MeasureName']})
	response = table.get_item(Key={'MeasureName': "NT - Administration state - Daily increase doses recorded"})
	actual_output = response['Item']
	assert actual_output == data


