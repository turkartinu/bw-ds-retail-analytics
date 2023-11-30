import boto3
import sys
# print("Before Append:", sys.path)

# sys.path.append('E:\\bwproject\\bw-ds-retail-analytics\\src\\utils')
# print("After Append:", sys.path)
from utils.vaultUtil import VaultClient
from utils.awsUtil import AWSConnector


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
# aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, region)
aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, region)


iam_client = aws_connector.aws_client_conn

response = iam_client.list_users()
for user in response['Users']:
    print('Username: {}'.format(user['UserName']))

