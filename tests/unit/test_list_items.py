import src.handlers.list_items as handler
from moto import mock_dynamodb2
import boto3
import json
import pytest
import os
ITEMS_TABLE_NAME = 'Items'


@mock_dynamodb2()
def test_list_items():
    dynamodb = boto3.resource('dynamodb')
    dynamodb.create_table(
        TableName=ITEMS_TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'item_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'item_id',
                'AttributeType': 'S'
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    table = dynamodb.Table(ITEMS_TABLE_NAME)
    data = [
        {'item_id': 'item_0001',
         'item_name': 'sample1', 'category': 'food'},
        {'item_id': 'item_0002',
         'item_name': 'sample2', 'category': 'food'},
        {'item_id': 'item_0003',
         'item_name': 'sample3', 'category': 'food'},
        {'item_id': 'item_0004',
         'item_name': 'sample4', 'category': 'merchandise'},
        {'item_id': 'item_0005',
         'item_name': 'sample5', 'category': 'merchandise'}
    ]
    for i in data:
        table.put_item(TableName=ITEMS_TABLE_NAME, Item=i)

    response = handler.list_items(20)
    assert response == data

    response2 = handler.list_items(3)
    assert len(response2) == 3