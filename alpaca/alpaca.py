#!/usr/bin/env python
"""
Alpaca
Builds Python modules on Amazon Linux using AWS CodeBuild and downloads them.
"""
__author__ = "Josh Campbell"
__version__ = "0.1.0"
__license__ = "MIT"
import subprocess
import boto3
from codebuild import create_build_project
from codebuild import build_artifact
from codebuild import delete_build_project


GET_AWS_ACCOUNT = "aws iam get-role --role-name 'CodeBuildTesting' "\
                  "--query 'Role.Arn' --output text"
DOWNLOAD_ARTIFACT = "aws s3 cp s3://rebukethe.net/alpacaBuilder/alpaca.zip ."
DELETE_ARTIFACT = "aws s3 rm s3://rebukethe.net/alpacaBuilder/alpaca.zip"


def create_client():
    """ Creates a new boto3 client """
    print("Creating boto3 client...")
    return boto3.client('codebuild')


def main():
    """ Main entry point of the app """
    print("Starting alpaca...")
    client = create_client()
    role = str(subprocess.check_output(GET_AWS_ACCOUNT, shell=True)
                         .decode(encoding='UTF-8')).rstrip()
    create_build_project(client, role)
    build_artifact(client)

    # Download the artifact.
    subprocess.run(DOWNLOAD_ARTIFACT.split(' '))

    # Cleanup phase.
    delete_build_project(client)
    subprocess.run(DELETE_ARTIFACT.split(' '))

    print("Exiting...")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
