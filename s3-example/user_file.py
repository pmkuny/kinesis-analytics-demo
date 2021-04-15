#!/usr/bin/env python3

import boto3
import os
import requests
import json
import uuid

# Global Variables
s3_client = boto3.client('s3', region_name='us-west-2')
api_endpoint = "https://randomuser.me/api/"
response_csv = requests.get(api_endpoint)

# data type URI format = https://randomuser.me/api/?format=[csv,xml,yaml,json,pretty]
# Using JSON for now
def get_data(endpoint,data_type):
    response_type = endpoint + "?format={}".format(data_type)
    response = requests.get(response_type)
    return(response.json())

# Open a file, get data, write data to file
get_data(api_endpoint,"json")

def write_file(filename,data):

    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
   
    if region is None:
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)
 
    return True

b_name = 's3demo-{}'.format(uuid.uuid4())
create_bucket(b_name, "us-west-2")