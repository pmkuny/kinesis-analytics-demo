#!/usr/bin/env python3

import boto3
import requests
import uuid
import botocore.exceptions

g_api_endpoint = "https://randomuser.me/api"
g_s3_client = boto3.client("s3")
g_firehose_client = boto3.client("firehose")
g_firehose_role_arn = 'arn:aws:iam::695507447459:role/KinesisFirehosetoS3'


def create_firehose_bucket(bucket_name):
    bucket_name = bucket_name + '-' + '{}'.format(uuid.uuid4())
    boto_response = g_s3_client.create_bucket(Bucket=bucket_name)
    return(bucket_name, boto_response)
    
    
    
def create_firehose_delivery_stream(delivery_stream_name,destination_bucket):
    if destination_bucket == None:
        destination_bucket = create_firehose_bucket("firehose")
    
    if delivery_stream_name == None:
        delivery_stream_name = 'firehoseds-' + '{}'.format(uuid.uuid4())
        
    try:
        g_firehose_client.create_delivery_stream(
            DeliveryStreamName=delivery_stream_name,
            DeliveryStreamType='DirectPut',
            ExtendedS3DestinationConfiguration={
                'RoleARN': g_firehose_role_arn,
                'BucketARN': 'arn:aws:s3:::{}'.format(destination_bucket)}
            )
    except ClientError as error:
        print("Testing Error")
        raise error
        
    
    
    
def get_user_api_data(api_endpoint):
    endpoint_response = requests.get(api_endpoint)
    endpoint_response_json = endpoint_response.json()
    return(endpoint_response_json)
        
        
        
        
    