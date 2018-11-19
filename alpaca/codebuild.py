"""
Administration of AWS CodeBuild Resources through a boto3 client.
"""
import time
import yaml


def generate_buildspec(package):
    """
    Creates a valid Buildspec, from a template, for an AWS CodeBuild project.
    The template requires a valid PyPi package to be specified.

    Parameters
    ----------
    package : str
        Name of the PyPi package to be built by AWS CodeBuild.

    Returns
    -------
    str
        The Buildspec in YAML.
    """
    return yaml.dump({
        "version": 0.2,
        "phases": {
            "build": {
                "commands": [
                    "pip-3.6 install {} -t alpaca".format(package),
                    "cd alpaca/",
                    "zip -r ../alpaca.zip *"
                ]
            }
        },
        "artifacts": {
            "files": [
                "alpaca.zip"
            ]
        }
    })


def create_build_project(client, role, bucket, buildspec):
    """
    Creates a new AWS CodeBuild Project to build the PyPi package(s).

    Parameters
    ----------
    client : botocore.client.S3
        A boto3 client for S3.
    role : str
        Name of the IAM Role the AWS CodeBuild project should use.
    bucket : str
        Name of the bucket the build artifact will be put in.
    buildspec : str
        A valid AWS CodeBuild Buildspec in YAML. Use s3.generate_buildspec().

    Returns
    -------
    dict
        boto3 response object. See https://boto3.amazonaws.com/v1/documentation
        /api/latest/reference/services
        /codebuild.html#CodeBuild.Client.create_project for more information.
    """
    print("Creating CodeBuild project...")
    try:
        response = client.create_project(
            name='alpacaBuilder',
            source={
                'type': 'NO_SOURCE',
                'buildspec': buildspec,
            },
            artifacts={
                'type': 'S3',
                'location': bucket,
            },
            environment={
                'type': 'LINUX_CONTAINER',
                'image': 'irlrobot/amazonlinux1:latest',
                'computeType': 'BUILD_GENERAL1_SMALL',
            },
            serviceRole=role,
        )
    except client.exceptions.ResourceAlreadyExistsException:
        print(">>alpacaBuilder project already exists, overwriting...")
        response = client.update_project(
            name='alpacaBuilder',
            source={
                'type': 'NO_SOURCE',
                'buildspec': buildspec,
            },
            artifacts={
                'type': 'S3',
                'location': bucket,
            },
            environment={
                'type': 'LINUX_CONTAINER',
                'image': 'irlrobot/amazonlinux1:latest',
                'computeType': 'BUILD_GENERAL1_SMALL',
            },
            serviceRole=role,
        )

    return response


def delete_build_project(client):
    """
    Deletes the Alpaca AWS CodeBuild project.

    Parameters
    ----------
    client : botocore.client.codebuild
        A boto3 client for CodeBuild.

    Returns
    -------
    """
    print("Deleting CodeBuild project...")
    client.delete_project(name="alpacaBuilder")


def wait_for_build_to_complete(client, build_id):
    """
    Keeps checking until a build completes.

    Parameters
    ----------
    client : botocore.client.codebuild
        A boto3 client for CodeBuild.

    build_id : str
        The ID of the AWS CodeBuild job to poll.

    Returns
    -------
    """
    response = client.batch_get_builds(ids=[build_id])
    # batch_get_builds() will return an array with one element.
    status = str(response.get('builds')[0].get('buildStatus'))
    if status == 'SUCCEEDED':
        print("Build completed...")
        return
    # TODO add case when status is FAILED
    else:
        print(">>Build {}, waiting 10 seconds...".format(status))
        time.sleep(10)
        # Recursively call until the build is done.
        return wait_for_build_to_complete(client, build_id)


def build_artifact(client):
    """
    Start a build and wait until it's done.

    Parameters
    ----------
    client : botocore.client.codebuild
        A boto3 client for CodeBuild.

    Returns
    -------
    """
    print("Submitting a build job for the specified package(s)...")
    response = client.start_build(projectName='alpacaBuilder')
    build_id = str(response.get('build').get('id'))
    print(">>Build ID is {}".format(build_id))
    wait_for_build_to_complete(client, build_id)
