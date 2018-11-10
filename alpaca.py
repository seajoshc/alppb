#!/usr/bin/env python
"""
Alpaca
Builds Python pip packages on Amazon Linux to ensure
compatability for programs using them on AWS Lambda.
"""
__author__ = "Josh Campbell"
__version__ = "0.1.0"
__license__ = "Apache2"
import boto3
from botocore.exceptions import ClientError


def create_build_project(client):
    """ Creates a new AWS CodeBuild Project to build the pip package(s)"""
    response = client.create_project(
        name='alpacaBuilder',
        source={
            'type': 'NO_SOURCE',
            'buildspec': '',
        },
        artifacts={
            'type': 'NO_ARTIFACTs',
        },
        environment={
            'type': 'LINUX_CONTAINER',
            'image': 'aws/codebuild/python:3.6.5-1.3.1',
            'computeType': 'BUILD_GENERAL1_SMALL',
        },
        serviceRole='',
    )


def create_client():
    """ Creates a new boto3 client """
    return boto3.client('codebuild')


def main():
    """ Main entry point of the app """
    client = create_client()
    create_build_project(client)
    print(client)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
