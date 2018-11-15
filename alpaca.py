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
import time
import boto3
from botocore.exceptions import ClientError


GET_AWS_ACCOUNT = "aws iam get-role --role-name 'CodeBuildTesting' --query 'Role.Arn' --output text"


def create_build_project(client, role):
    """ Creates a new AWS CodeBuild Project to build the pip package(s)"""
    print("Creating build project...")
    response = client.create_project(
        name='alpacaBuilder',
        source={
            'type': 'NO_SOURCE',
            'buildspec': base64.b64decode("dmVyc2lvbjogMC4yICAgICAgICAgCnBoYXNlczoKICBidWlsZDoKICAgIGNvbW1hbmRzOgogICAgICAtIHBpcCBpbnN0YWxsIHJlcXVlc3RzIC10IHBpcGJ1aWxkCmFydGlmYWN0czoKICBmaWxlczoKICAgIC0gJ3BpcGJ1aWxkLyoqLyonCiAgbmFtZTogcGlwYnVpbGQuemlw").decode(encoding='UTF-8'),
        },
        artifacts={
            'type': 'S3',
            'location': 'rebukethe.net',
        },
        environment={
            'type': 'LINUX_CONTAINER',
            'image': 'aws/codebuild/python:3.6.5-1.3.1',
            'computeType': 'BUILD_GENERAL1_SMALL',
        },
        serviceRole=role,
    )

    return response


def delete_build_project(client):
    """ Deletes an AWS CodeBuild project """
    print("Deleting build project and cleaning up...")
    client.delete_project(name="alpacaBuilder")


def get_artifact_location(client, build_id):
    """ Keeps checking until a build completes
    and then gets location of the artifact """
    response = client.batch_get_builds(ids=[build_id])
    # batch_get_builds() will return an array with one element.
    status = response.get('builds')[0].get('buildStatus')
    print("Build status is {}".format(status))
    if status == 'SUCCEEDED':
        print("Build completed...")
        # Build is done, return the artifact location.
        return str(response.get('builds')[0].get('artifacts').get('location'))
    else:
        print("Build not done, waiting 10 seconds...")
        time.sleep(10)
        # Recursively call until the build is done.
        return get_artifact_location(client, build_id)


def build_artifact(client):
    """ Start a build and get the location of the artifact """
    print("Starting build job...")
    response = client.start_build(projectName='alpacaBuilder')
    build_id = str(response.get('build').get('id'))
    print("Build ID is {}".format(build_id))
    artifact_location = get_artifact_location(client, build_id)
    print("Built module(s) located at {}".format(artifact_location))

    return str(artifact_location)


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
    build_artifact(client)
    delete_build_project(client)

    print("Exiting...")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
