import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    endpoint_url='http://localstack:4566'  # LocalStack URL within Docker Compose
)
table_name = 'ExchangeRates'
table = dynamodb.Table(table_name)

def create_exchange_rates_table():
    """Create the ExchangeRates table in DynamoDB if it doesn't exist."""
    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'Currency', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'Date', 'KeyType': 'RANGE'},    # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'Currency', 'AttributeType': 'S'},
                {'AttributeName': 'Date', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table {table_name} created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists.")
        else:
            print(f"Unexpected error: {e}")


def store_exchange_rate(currency, rate, date):
    """Store exchange rate in DynamoDB."""
    table.put_item(
        Item={
            'Currency': currency,
            'Rate': rate,
            'Date': date
        }
    )


def get_rates_by_date(date):
    """Retrieve exchange rates for a specific date from DynamoDB."""
    response = table.scan(
        FilterExpression="#date = :date",
        ExpressionAttributeNames={"#date": "Date"},
        ExpressionAttributeValues={":date": date}
    )
    return response.get('Items', [])
