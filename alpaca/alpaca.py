#!/usr/bin/env python
"""
Alpaca
Builds Python modules on Amazon Linux using AWS CodeBuild and downloads them.
"""
__author__ = "Josh Campbell"
__version__ = "0.1.0"
__license__ = "MIT"
import subprocess
import time
import boto3
import codebuild
import iam


DOWNLOAD_ARTIFACT = "aws s3 cp s3://rebukethe.net/alpacaBuilder/alpaca.zip ."
DELETE_ARTIFACT = "aws s3 rm s3://rebukethe.net/alpacaBuilder/alpaca.zip"


def create_client(resource):
    """ Creates a new boto3 client """
    print("Creating boto3 client for {}...".format(resource))
    return boto3.client(resource)


def main():
    """ Main entry point of the app """
    print("Starting alpaca...")
    iam_client = create_client('iam')
    codebuild_client = create_client('codebuild')
    role = iam.create_role(iam_client)
    # TODO be smarter about checking if the role is ready
    print("Waiting 10 seconds for IAM Role propagation before continuing...")
    time.sleep(10)
    codebuild.create_build_project(codebuild_client, role)
    codebuild.build_artifact(codebuild_client)

    # Download the artifact.
    subprocess.run(DOWNLOAD_ARTIFACT.split(' '))

    # Cleanup phase.
    codebuild.delete_build_project(codebuild_client)
    iam.delete_role(iam_client)
    subprocess.run(DELETE_ARTIFACT.split(' '))

    print("Exiting...")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
