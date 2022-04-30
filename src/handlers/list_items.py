import json
import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel('DEBUG')


def list_items(limit, last_key=None):
    logging.debug(limit)
    dynamodb = boto3.resource('dynamodb')
    TABLE_NAME = 'Items'
    table = dynamodb.Table(TABLE_NAME)

    scan_kwargs = {
        'ConsistentRead': True,
        'Limit': limit
    }

    if last_key:
        scan_kwargs['ExclusiveStartKey'] = last_key

    response = table.scan(**scan_kwargs)
    logging.info(response)
    items = response.get('Items', [])
    return items


def handler(event, context):
    try:
        logging.info(event)
        logging.info(context)
        
        result = list_items(int(os.environ['DEFAULT_DATA_LIMIT']))
        logging.debug(result)
        return {
            'statusCode': 200,
            # ensure_ascii: 日本語文字化け対応
            'body': json.dumps(result, ensure_ascii=False)
        }

    except Exception as e:
        logging.error(e)