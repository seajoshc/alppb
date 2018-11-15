#!/usr/bin/env python
"""
Alpaca
Builds Python modules on Amazon Linux using AWS CodeBuild and downloads them.
"""
__author__ = "Josh Campbell"
__version__ = "0.1.0"
__license__ = "MIT"
import time
import boto3
import codebuild
import iam
import s3


def create_client(service):
    """ Creates a new boto3 client """
    print("Creating boto3 client for {}...".format(service))
    return boto3.client(service)


def create_resource(service):
    """
    Creates a boto3 resource object for the specified service.

    Parameters
    ----------
    service : str
        The name of the AWS service to create the resource for.

    Returns
    -------
    boto3.resources.factory.service.ServiceResource
    """
    return boto3.resource(service)


def main():
    """ Main entry point of the app """
    print("Starting alpaca...")
    # Create boto3 clients/resources used below.
    iam_client = create_client('iam')
    codebuild_client = create_client('codebuild')
    s3_resource = create_resource('s3')
    s3_client = create_client('s3')

    # Hardcoded bucket during development.
    bucket = 'rebukethe.net'

    # Create Alpaca resources.
    role = iam.create_role(iam_client)
    # TODO be smarter about checking if the role is ready
    print("Waiting 10 seconds for IAM Role propagation before continuing...")
    time.sleep(10)
    codebuild.create_build_project(codebuild_client, role)
    codebuild.build_artifact(codebuild_client)

    # Download the artifact.
    s3.download_artifact(s3_resource, bucket)

    # Cleanup phase.
    codebuild.delete_build_project(codebuild_client)
    iam.delete_role(iam_client)
    s3.delete_artifact(s3_client, bucket)

    print("Exiting...")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
