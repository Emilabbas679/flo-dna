import random
import re
import logging
import os.path as op
import requests
from flask import jsonify, current_app
from werkzeug.utils import secure_filename

import requests
from flask import jsonify, current_app
from werkzeug.utils import secure_filename

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError


# presigned url for uploadin file from front-end
def create_presigned_post(bucket_name, object_name,
                          fields=None, conditions=None, expiration=3600):
    session = boto3.session.Session()
    s3_client = session.client(
        "s3",
        region_name="fra1",
        endpoint_url="https://fra1.digitaloceanspaces.com",
        aws_access_key_id="UKZLL2BAK4F7WCCXYIBD",
        aws_secret_access_key="jDqe3BIu9J7x+/i0XgRrcuw9+ZFEiWhTKo3J2Vsly1E"
    )
    s3_file_key = op.join('landing-pages', object_name)

    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     s3_file_key,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)

    except ClientError as e:
        logging.error(e)
        return None

    return response


# presigned url for uploaded file for view
def create_presigned_url(bucket_name, object_name, expiration=3600):
    session = boto3.session.Session()
    s3_client = session.client(
        "s3",
        region_name="fra1",
        endpoint_url="https://fra1.digitaloceanspaces.com",
        aws_access_key_id="UKZLL2BAK4F7WCCXYIBD",
        aws_secret_access_key="jDqe3BIu9J7x+/i0XgRrcuw9+ZFEiWhTKo3J2Vsly1E"
    )
    s3_file_key = op.join('landing-pages', object_name)

    try:
        response = s3_client.generate_presigned_url(ClientMethod='get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': s3_file_key},
                                                    ExpiresIn=300)

    except ClientError as e:
        logging.error(e)
        return None

    return response


# upload file to digital ocean spaces from backend
def upload_file_to_spaces(bucket_name, uploaded_file, key, content_type, permission):
    session = boto3.session.Session()
    s3_client = session.client(
        "s3",
        region_name=current_app.config['S3_REGION_NAME'],
        endpoint_url=current_app.config['S3_ENDPOINT_URL'],
        aws_access_key_id=current_app.config['S3_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['S3_SECRET_ACCESS_KEY']
    )

    try:

        response = s3_client.put_object(Body=uploaded_file, Bucket=bucket_name,
                                        Key=key,
                                        ACL=permission, ContentType=content_type)

    except ClientError as e:
        logging.error(e)
        return None

    return response


def delete_file_from_spaces(bucket_name, key):
    session = boto3.session.Session()
    s3_client = session.client(
        "s3",
        region_name=current_app.config['S3_REGION_NAME'],
        endpoint_url=current_app.config['S3_ENDPOINT_URL'],
        aws_access_key_id=current_app.config['S3_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['S3_SECRET_ACCESS_KEY']
    )

    try:

        response = s3_client.delete_object(Bucket=bucket_name, Key=key)

    except ClientError as e:
        logging.error(e)
        return None

    return response


def upload_file():
    pass


def generate_sku():
    number = random.randrange(100000, 999999)
    return f'FLO-{number}'
