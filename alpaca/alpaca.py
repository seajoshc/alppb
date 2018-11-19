#!/usr/bin/env python
"""
Alpaca
Builds Python modules on Amazon Linux using AWS CodeBuild and downloads them.
"""
__author__ = "Josh Campbell"
__version__ = "0.1.0"
__license__ = "MIT"
import argparse
import time
import boto3
from . import codebuild
from . import iam
from . import s3


def preflight_check():
    """
    Checks if all pre-requisites are in place before trying to run Alpaca.
    Checks include:
        - Are boto3 credentials available?

    Parameters
    ----------

    Returns
    -------
    """
    session = boto3.Session()
    credentials = session.get_credentials()
    if credentials is None:
        print("ERROR: boto3 credentials missing. "
              "Does ~/.aws/credentials exist?")
        exit(1)


def create_client(service):
    """
    Creates a boto3 client object for the specified service.

    Parameters
    ----------
    service : str
        The name of the AWS service to create the client for.

    Returns
    -------
    botocore.client.service
        See https://boto3.amazonaws.com/v1/documentation/api/latest/guide
        /clients.html for more information.
    """
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
        See https://boto3.amazonaws.com/v1/documentation/api/latest/guide
        /resources.html for more information.
    """
    print("Creating boto3 resource for {}...".format(service))
    return boto3.resource(service)


def main():
    """ Main entry point of the app """
    print("Starting alpaca...")
    preflight_check()

    # Parsing arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("package", help="The PyPi package you want to build.")
    parser.add_argument("bucket", help="Name of the S3 bucket to use.")
    args = parser.parse_args()
    bucket = str(args.bucket)

    # Create boto3 clients/resources used below.
    iam_client = create_client('iam')
    codebuild_client = create_client('codebuild')
    s3_resource = create_resource('s3')
    s3_client = create_client('s3')

    # Create Alpaca resources.
    role = iam.create_role(iam_client, bucket)
    # TODO be smarter about checking if the role is ready
    print(">>Waiting 10 seconds for IAM Role propagation before continuing...")
    time.sleep(10)
    buildspec = codebuild.generate_buildspec(str(args.package))
    codebuild.create_build_project(codebuild_client, role, bucket, buildspec)
    codebuild.build_artifact(codebuild_client)

    # Download the artifact.
    s3.download_artifact(s3_resource, bucket)

    # Cleanup phase.
    codebuild.delete_build_project(codebuild_client)
    iam.delete_role(iam_client)
    s3.delete_artifact(s3_client, bucket)

    print("SUCCESS")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
