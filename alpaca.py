#!/usr/bin/env python
"""
Alpaca
Builds Python pip packages on Amazon Linux to ensure
compatability for programs using them on AWS Lambda.
"""
__author__ = "Josh Campbell"
__version__ = "0.1.0"
__license__ = "Apache2"
import base64
import subprocess
import boto3
from botocore.exceptions import ClientError


GET_AWS_ACCOUNT = "aws iam get-role --role-name 'CodeBuildTesting' --query 'Role.Arn' --output text"


def create_build_project(client, role):
    """ Creates a new AWS CodeBuild Project to build the pip package(s)"""
    print("Creating build project...")
    client.create_project(
        name='alpacaBuilder',
        source={
            'type': 'NO_SOURCE',
            'buildspec': base64.b64decode("dmVyc2lvbjogMC4yICAgICAgICAgCnBoYXNlczoKICBidWlsZDoKICAgIGNvbW1hbmRzOgogICAgICAtIHBpcCBpbnN0YWxsIHJlcXVlc3RzIC10IHBpcGJ1aWxkCmFydGlmYWN0czoKICBmaWxlczoKICAgIC0gJ3BpcGJ1aWxkLycKICBuYW1lOiBwaXBidWlsZC56aXA=").decode(encoding='UTF-8'),
        },
        artifacts={
            'type': 'S3',
            'location': 'rebukethe.net'
        },
        environment={
            'type': 'LINUX_CONTAINER',
            'image': 'aws/codebuild/python:3.6.5-1.3.1',
            'computeType': 'BUILD_GENERAL1_SMALL',
        },
        serviceRole=role,
    )


def delete_build_project(client):
    """ Deletes an AWS CodeBuild project """
    print("Deleting build project...")
    client.delete_project(name="alpacaBuilder")


def create_client():
    """ Creates a new boto3 client """
    print("Creating boto3 client...")
    return boto3.client('codebuild')


def main():
    """ Main entry point of the app """
    print("Starting alpaca...")
    client = create_client()
    role = str(subprocess.check_output(GET_AWS_ACCOUNT, shell=True).decode(encoding='UTF-8')).rstrip()
    create_build_project(client, role)
    delete_build_project(client)
    print(client)
    print("Exiting...")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
