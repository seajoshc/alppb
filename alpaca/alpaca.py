#!/usr/bin/env python
"""
Alpaca
Builds Python modules on Amazon Linux using AWS CodeBuild and downloads them.
"""
__author__ = "Josh Campbell"
__version__ = "0.1.0"
__license__ = "MIT"
import argparse
import boto3
from botocore.exceptions import NoRegionError
from . import codebuild
from . import iam
from . import s3


def check_for_boto_credentials():
    """
    Checks if credentials for boto3 to use are available.

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


def create_client(service, region):
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
    try:
        return boto3.client(service, region_name=region)
    except NoRegionError:
        print("ERROR: boto3 cannot find a default profile to use. Try running "
              "`aws configure`. To see how boto3 loads configuration, see: "
              "https://boto3.amazonaws.com/v1/documentation/api/latest/guide/"
              "configuration.html#configuring-credentials")
        exit(1)


def create_resource(service, region):
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
    try:
        return boto3.resource(service, region_name=region)
    except NoRegionError:
        print("ERROR: boto3 cannot find a default profile to use. Try running "
              "`aws configure`. To see how boto3 loads configuration, see: "
              "https://boto3.amazonaws.com/v1/documentation/api/latest/guide/"
              "configuration.html#configuring-credentials")
        exit(1)


def main():
    """ Main entry point of the app """
    print("Starting alpaca...")
    check_for_boto_credentials()

    # Parsing arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("package", help="The PyPi package you want to build.")
    parser.add_argument("bucket", help="Name of the S3 bucket to use.",
                        type=str)
    parser.add_argument("--region", help="The AWS region to use.", type=str)
    args = parser.parse_args()
    bucket = args.bucket
    # If region is None boto3 will determine the region to use. See more at,
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide
    # /configuration.html#configuring-credentials
    region = args.region

    # Try to use boto3 profile default region if region arg wasn't used.

    # Create boto3 clients/resources used below.
    iam_client = create_client('iam', region)
    codebuild_client = create_client('codebuild', region)
    s3_resource = create_resource('s3', region)
    s3_client = create_client('s3', region)

    # Create Alpaca resources.
    role = iam.create_role(iam_client, bucket)
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
