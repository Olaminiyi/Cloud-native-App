import boto3
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

client = boto3.client('ecr')

repository_name = "my_monitoring_app_image"
response = client.create_repository(repositoryName=repository_name)

repository_uri = response['repository'] ['repositoryUri']
print(repository_uri)