#!/usr/bin/env python3

import boto3
import requests
import uuid

endpoint = "https://randomuser.me/api"


def get_firehose(bucket_name):
    fireclient = boto3.client('firehose')
    create_response = fireclient.create_delivery_stream(
        DeliveryStreamName='{}'.format(uuid.uuid4()),
        DeliveryStreamType='DirectPut',
        ExtendedS3DestinationConfiguration={
            'RoleARN': 'string',
            'BucketARN': 'arn:aws:s3:::{}'.format(bucket_name),
            'ErrorOutputPrefix': 'err-'})
    return(create_response)
            
       
    
def create_s3(bucket_name):
    s3client = boto3.client('s3')
    b_name = bucket_name + '-' + '{}'.format(uuid.uuid4())
    response = s3client.create_bucket(Bucket=b_name)
    print(response)
    return(b_name)
    


def get_user():
    user_response = requests.get(endpoint)
    user_response_data = user_response.json()
    
    for user in user_response_data["results"]:
        print(user["gender"])
        
        
    print(user_response)    
    print(user_response_data)


get_user()
b_name = print(create_s3("test"))
print(get_firehose(b_name))
