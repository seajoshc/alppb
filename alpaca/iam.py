"""
Administration of AWS IAM Resources through a boto3 client.
"""
import base64


def create_role(client):
    """
    Creates an IAM Role to use with AWS CodeBuild

    Parameters
    ----------
    client : botocore.client.iam
        A boto3 client for IAM.

    Returns
    -------
    str
        ARN of the newly created IAM Role.
    """
    print("Creating IAM Role...")
    response = client.create_role(
        RoleName='alpacaBuilderRole',
        AssumeRolePolicyDocument=str(base64.b64decode(
            """
            ewogICJWZXJzaW9uIjogIjIwMTItMTAtMTciLAogICJTdGF0ZW1lbnQiOiBbCiAgICB
            7CiAgICAgICJFZmZlY3QiOiAiQWxsb3ciLAogICAgICAiUHJpbmNpcGFsIjogewogIC
            AgICAgICJTZXJ2aWNlIjogImNvZGVidWlsZC5hbWF6b25hd3MuY29tIgogICAgICB9L
            AogICAgICAiQWN0aW9uIjogInN0czpBc3N1bWVSb2xlIgogICAgfQogIF0KfQ==
            """).decode(encoding='UTF-8')),
        Description='This role is used by https://github.com/irlrobot/alpaca',
    )
    add_role_policy(client)

    return str(response.get('Role').get('Arn'))


def add_role_policy(client):
    """
    Adds an IAM Policy to a newly created IAM Role from iam.create_role().

    Parameters
    ----------
    client : botocore.client.iam
        A boto3 client for IAM.

    Returns
    -------
    """
    print(">>Attaching Policy to the the IAM Role...")
    client.put_role_policy(
        RoleName='alpacaBuilderRole',
        PolicyName='alpacaBuilderPolicy',
        PolicyDocument=str(base64.b64decode(
            """
            ewogICAgIlZlcnNpb24iOiAiMjAxMi0xMC0xNyIsCiAgICAiU3RhdGVtZW50Ijo
            gWwogICAgICAgIHsKICAgICAgICAgICAgIlNpZCI6ICJDbG91ZFdhdGNoTG9nc1
            BvbGljeSIsCiAgICAgICAgICAgICJFZmZlY3QiOiAiQWxsb3ciLAogICAgICAgI
            CAgICAiQWN0aW9uIjogWwogICAgICAgICAgICAgICAgImxvZ3M6Q3JlYXRlTG9n
            R3JvdXAiLAogICAgICAgICAgICAgICAgImxvZ3M6Q3JlYXRlTG9nU3RyZWFtIiw
            KICAgICAgICAgICAgICAgICJsb2dzOlB1dExvZ0V2ZW50cyIKICAgICAgICAgIC
            AgXSwKICAgICAgICAgICAgIlJlc291cmNlIjogWwogICAgICAgICAgICAgICAgI
            ioiCiAgICAgICAgICAgIF0KICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAg
            ICAgIkVmZmVjdCI6ICJBbGxvdyIsCiAgICAgICAgICAgICJBY3Rpb24iOiBbCiA
            gICAgICAgICAgICAgICAiczM6TGlzdEJ1Y2tldCIKICAgICAgICAgICAgXSwKIC
            AgICAgICAgICAgIlJlc291cmNlIjogWwogICAgICAgICAgICAgICAgImFybjphd
            3M6czM6OjpyZWJ1a2V0aGUubmV0IgogICAgICAgICAgICBdCiAgICAgICAgfSwK
            ICAgICAgICB7CiAgICAgICAgICAgICJFZmZlY3QiOiAiQWxsb3ciLAogICAgICA
            gICAgICAiQWN0aW9uIjogWwogICAgICAgICAgICAgICAgInMzOlB1dE9iamVjdC
            IsCiAgICAgICAgICAgICAgICAiczM6R2V0T2JqZWN0IiwKICAgICAgICAgICAgI
            CAgICJzMzpEZWxldGVPYmplY3QiCiAgICAgICAgICAgIF0sCiAgICAgICAgICAg
            ICJSZXNvdXJjZSI6IFsKICAgICAgICAgICAgICAgICJhcm46YXdzOnMzOjo6cmV
            idWtldGhlLm5ldC8qIgogICAgICAgICAgICBdCiAgICAgICAgfQogICAgXQp9
            """).decode(encoding='UTF-8')),
    )


def delete_role(client):
    """
    Deletes an IAM Role created from iam.create_role().

    Parameters
    ----------
    client : botocore.client.iam
        A boto3 client for IAM.

    Returns
    -------
    """
    print("Deleting IAM Role...")
    # AWS API wants all role policies deleted before the role itself.
    # TODO get all policies on the role and then delete in case it was modified
    client.delete_role_policy(
        RoleName='alpacaBuilderRole',
        PolicyName='alpacaBuilderPolicy'
    )
    client.delete_role(RoleName='alpacaBuilderRole')
