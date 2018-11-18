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
import codebuild
import iam
import s3


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


def force_cleanup(codebuild_client, iam_client):
    """
    Deletes the IAM Role and CodeBuild project Alpaca creates. This is useful
    for when Alpaca doesn't gracefully exit and dangling resources need to be
    destroyed. This will not delete anything except the IAM Role named
    \"alpacaBuilderRole\" and the CodeBuild project named \"alpacaBuilder\".
    Specifically, this will not delete any S3 buckets or objects in S3.

    Parameters
    ----------
    codebuild_client : botocore.client.codebuild
        A boto3 client for CodeBuild.

    iam_client : botocore.client.iam
        A boto3 client for IAM.

    Returns
    -------
    """
    print("Forcing a cleanup...")
    try:
        codebuild.delete_build_project(codebuild_client)
        print(">>Deleted CodeBuild project...")
    except:
        print(">>No CodeBuild project to delete, skipping...")

    try:
        iam.delete_role(iam_client)
        print(">>Deleted IAM Role...")
    except:
        print(">>No IAM Role to delete, skipping...")


def main():
    """ Main entry point of the app """
    print("Starting alpaca...")

    # Parsing arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("package", help="The PyPi package you want to build.")
    parser.add_argument("bucket", help="Name of the S3 bucket to use.")
    parser.add_argument("-c", "--cleanup",
                        help="Force a cleanup of any and all Alpaca resources"
                        " in AWS. Useful if Alpaca did not gracefully exit.",
                        action="store_true")
    args = parser.parse_args()

    # Create boto3 clients/resources used below.
    iam_client = create_client('iam')
    codebuild_client = create_client('codebuild')
    s3_resource = create_resource('s3')
    s3_client = create_client('s3')

    # Handle --cleanup.
    if args.cleanup:
        force_cleanup(codebuild_client, iam_client)

    # Create Alpaca resources.
    bucket = str(args.bucket)
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
