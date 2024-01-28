import os
import boto3
from botocore.client import BaseClient
from botocore.exceptions import NoCredentialsError
import requests


# Replace there values with environment variable with values that match your access key
aws_access_key = os.environ.get('S3_POC_AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('S3_POC_AWS_SECRET_ACCESS_KEY')

# Replace there values with environment variable with values that match your setup
s3_region = os.environ.get('S3_POC_REGION')
bucket_name_public = os.environ.get('S3_POC_PUBLIC')
bucket_name_private = os.environ.get('S3_POC_PRIVATE')

# Create an S3 client
s3_with_creds = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# Create an S3 client without credentials
s3_with_no_creds = boto3.client('s3')

s3_file_added_manually = "junk_manual.txt"

# S3 file link
s3_public_link_to_manually_uploaded_file = f'https://{bucket_name_public}.s3.{s3_region}.amazonaws.com/{s3_file_added_manually}'
s3_private_link_to_manually_uploaded_file = f'https://{bucket_name_private}.s3.{s3_region}.amazonaws.com/{s3_file_added_manually}'

# Specify local file path for download
download_to_file_path_public = 'Data/public/downloaded_file.txt'
download_to_file_path_public_via_boto = 'Data/public/downloaded_file_boto.txt'
download_to_file_path_private_denied_expected = 'Data/Private/downloaded_file_expect_denied.txt'
download_to_file_path_private_via_boto = 'Data/Private/downloaded_file_boto.txt'


def validate_access_environment_variables():
    # Check if the environment variable is set
    if aws_access_key is not None:
        print(f"AWS Access Key ID: {aws_access_key}")
    else:
        raise ValueError("Environment variable PREFECT_AWS_ACCESS_KEY_ID is not set.")


def validate_s3_environment_variables():

    report_env_var_valid("S3_POC_PUBLIC", s3_public_link_to_manually_uploaded_file, "Public link")
    report_env_var_valid("S3_POC_PRIVATE", s3_private_link_to_manually_uploaded_file,  "Private link")
    report_env_var_valid("S3_POC_REGION", s3_region, "Region")


def report_env_var_valid(name: str, value, label: str):
    if value is not None:
        print(f"{label} is : {value}")
    else:
        raise ValueError(f"Environment variable {name} is not set.")


def download_file_from_s3_using_http_direct(link, local_path):
    try:
        response = requests.get(link)
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully to {local_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")


def upload_file_to_s3(boto_client: BaseClient, local_path, bucket, s3_key):
    try:
        boto_client.upload_file(local_path, bucket, s3_key)
        print(f"File uploaded successfully to S3 bucket {bucket} with key {s3_key}")
    except NoCredentialsError:
        print("AWS credentials not available")


def download_file_from_s3(boto_client: BaseClient, bucket, s3_key, local_path):
    try:
        # Download the file
        boto_client.download_file(bucket, s3_key, local_path)
        print(f"File downloaded successfully to {local_path}")
    except NoCredentialsError:
        print("AWS credentials not available")
    except Exception as e:
        print(f"Error downloading file: {e}")


def public_repo_actions(s3_key_for_upload: str):
    bucket_name = bucket_name_public

    # ---- Download the file from S3
    # - No Credentials via BOTO as public
    download_file_from_s3(s3_with_no_creds,
                          bucket_name,
                          s3_file_added_manually,
                          download_to_file_path_private_via_boto)

    # - No Credentials via http as public
    download_file_from_s3_using_http_direct(s3_public_link_to_manually_uploaded_file, download_to_file_path_public)

    # Upload the downloaded file to S3 (again no creds as public)
    upload_file_to_s3(s3_with_no_creds,
                      download_to_file_path_public,
                      bucket_name_public,
                      s3_key_for_upload)


def private_repo_actions(s3_key_for_upload: str):

    bucket_name = bucket_name_private

    # Download the file from S3 with credentials as private
    download_file_from_s3(s3_with_creds,
                          bucket_name,
                          s3_file_added_manually,
                          download_to_file_path_private_via_boto)

    # Try to download the file from S3 using http directly should get access denied
    download_file_from_s3_using_http_direct(s3_private_link_to_manually_uploaded_file, download_to_file_path_private_denied_expected)

    upload_file_to_s3(s3_with_creds,
                      download_to_file_path_private_via_boto,
                      bucket_name,
                      s3_key_for_upload)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    validate_s3_environment_variables()
    validate_access_environment_variables()

    public_repo_actions('uploaded_file_pub.txt')

    private_repo_actions('uploaded_file_private.txt')














