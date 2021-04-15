#!/usr/bin/env python3

import boto3
import requests
import uuid
import botocore.exceptions

# Defining global variables for our various services clients.
g_api_endpoint = "https://randomuser.me/api"
g_s3_client = boto3.client("s3")
g_firehose_client = boto3.client("firehose", region_name='us-west-2')
g_firehose_role_arn = 'arn:aws:iam::695507447459:role/KinesisFirehosetoS3'

# The create_delivery_stream method of Firehose requires one of several destinations.
# We're using S3 here so we'll use this function to create an S3 bucket.
def create_firehose_bucket(bucket_name):
    bucket_name = bucket_name + '-' + '{}'.format(uuid.uuid4())
    boto_response = g_s3_client.create_bucket(Bucket=bucket_name)
    return(bucket_name, boto_response)
    
    
    
def create_firehose_delivery_stream(delivery_stream_name,destination_bucket):
    destination_bucket = create_firehose_bucket("firehose")
    
    if delivery_stream_name == None:
        delivery_stream_name = 'firehoseds-' + '{}'.format(uuid.uuid4())
        
    # Role ARN is specifying the universal identifier (ARN) of the IAM Role that Firehose will use to write to the S3 bucket.
    # Bucket ARN is meant to be dynamic and based on bucket name.
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
        
    
    
# Run in parallel to get the user API data. Store as JSON.
def get_user_api_data(api_endpoint):
    endpoint_response = requests.get(api_endpoint)
    endpoint_response_json = endpoint_response.json()
    return(endpoint_response_json)
        
        
        
        
    