import boto3
import sys
# print("Before Append:", sys.path)
#import utils
# sys.path.append('c:\\workspace\\bwprojects\\snowflakeDemo\\bw-des-retail-analytics\\utils')
# print("After Append:", sys.path)
from vaultUtil import VaultClient
from awsUtil import AWSConnector
from snowUtil import SnowflakeConnector

VAULT_URL = "http://127.0.0.1:8200"
ROLE_ID = "f1415db9-3ff3-5a07-7813-3afc6f2e8620"
SECRET_ID = "e6d81399-98cc-6a30-8e66-5234e3a2f3f3"
SECRET_PATH = "secret/data/aws"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        print("Secret data:", secret_data)
    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")


aws_access_key = secret_data['data']['bw-aws-accesskey-dev']
aws_secret_key = secret_data['data']['bw-aws-secret-dev']

region = 'us-east-1'  # Replace with your preferred AWS region


client='iam'
aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, region)

# Access the S3 client through the instance
iam_client = aws_connector.aws_client_conn

# Now you can use s3_client to perform S3 operations
response = iam_client.list_groups()

print("IAM groups:", response)



# Replace these with your Snowflake account details
account = 'emb85346.us-east-1'

SECRET_PATH = "secret/data/snow"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        print("Secret data:", secret_data)
    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")


user = secret_data['data']['bw-snow-serviceusername-dev']
password = secret_data['data']['bw-snow-servicepassword-dev']


warehouse = 'COMPUTE_WH'
database = 'SNOWFLAKE_SAMPLE_DATA'
schema = 'TPCH_SF1'

# Create an instance of SnowflakeConnector
snowflake_conn = SnowflakeConnector(account, user, password, warehouse, database, schema)

# Connect to Snowflake
snowflake_conn.connect()

# Execute a query
query_result = snowflake_conn.execute_query("SELECT * from SUPPLIER limit 5")

# Print the result
print("Current Data in Snowflake:", query_result[0][0])

# Close the connection
snowflake_conn.close_connection()