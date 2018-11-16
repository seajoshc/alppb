"""
Administration of Amazon S3 Resources through a boto3 client.
"""


def download_artifact(resource, bucket, key='alpacaBuilder/alpaca.zip',
                      local_path='alpaca.zip'):
    """
    Fetches the artifact from Amazon S3 built by Alpaca .

    Parameters
    ----------
    resource : boto3.resources.factory.s3.ServiceResource
        A boto3 Resource interface for S3.
    bucket : str
        Name of the bucket the artifact exists in.
    key: str
        The S3 key of the artifact to download from the bucket. Defaults to
        "alpacaBuilder/alpaca.zip".
    local_path: str
        The local path where the artifact will be downloaded. Defaults to the
        current directory Alpaca is being run from.

    Returns
    -------
    """
    print("Downloading built package(s) to {}...".format(local_path))
    resource.meta.client.download_file(bucket, key, local_path)
    print("Download complete...")


def delete_artifact(client, bucket, key='alpacaBuilder/alpaca.zip'):
    """
    Deletes the artifact from Amazon S3 built by Alpaca.

    Parameters
    ----------
    client : botocore.client.S3
        A boto3 client for S3.
    bucket : str
        Name of the bucket the artifact exists in.
    key: str
        The S3 key of the artifact to delete from the bucket. Defaults to
        "alpacaBuilder/alpaca.zip".

    Returns
    -------
    """
    print("Deleting {} from S3 bucket {}...".format(key, bucket))
    client.delete_object(Bucket=bucket, Key=key)
