import boto3
import json


sts_client = boto3.client("sts")


def init_secret_client(role_arn: str, region):
    try:
        assumed_role_object = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="Operations",
        )
        return boto3.client(
            "secretsmanager",
            region_name=region,
            aws_access_key_id=assumed_role_object["Credentials"]["AccessKeyId"],
            aws_secret_access_key=assumed_role_object["Credentials"]["SecretAccessKey"],
            aws_session_token=assumed_role_object["Credentials"]["SessionToken"],
        )
    except Exception as e:
        print(e)
        return None


def manage_secrets(account_secret) -> None:
    # secret_client = boto3.client("secretsmanager", region_name="ap-southeast-1")
    secret_client = init_secret_client(
        account_secret["role_arn"], account_secret["region"]
    )
    for secret in account_secret["secrets"]:
        aws_secret = describe_secret(client=secret_client, secret_id=secret["name"])
        if secret["status"] == "inactive":
            delete_secret(client=secret_client, secret_id=secret["name"])
            continue
        # Describe secret
        # aws_secret = describe_secret(client=secret_client, secret_id=secret["name"])
        # create_secret(client=client, secret=secret)
        if aws_secret:
            # Update value
            put_secret_value(client=secret_client, secret=secret)
            continue
        # Create secret
        create_secret(client=secret_client, secret=secret)


def put_secret_value(client, secret: dict) -> None:
    try:
        client.put_secret_value(
            SecretId=secret["name"],
            SecretString=json.dumps(secret["value"]),
        )
        print(f"Secret {secret['name']} value has been updated")
    except Exception as e:
        print(f"Something went wrong when update secret {secret['name']}: {e}")


def create_secret(client, secret: dict) -> None:
    # Create secret if not existed
    try:
        response = client.create_secret(
            Name=secret["name"],
            Description=secret["description"],
            SecretString=json.dumps(secret["value"]),
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            print(f"Secret {secret['name']} has been created!")
    except Exception as e:
        print(f"Something else went wrong when create secret {secret['name']}: {e}")


def describe_secret(client, secret_id) -> dict:
    try:
        response = client.describe_secret(SecretId=secret_id)
    except client.exceptions.ResourceNotFoundException:
        return None
    except Exception as e:
        print(f"Something else went wrong with secret {secret_id}: {e} ")
    return response


def delete_secret(client, secret_id):
    try:
        client.delete_secret(
            SecretId=secret_id,
            ForceDeleteWithoutRecovery=True,
        )
        print(f"Secret {secret_id} has been removed")
    except Exception as e:
        print(e)
