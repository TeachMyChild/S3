# S3 Example

Simple example of how to use S3 for public and private buckets

## Permissions

A user was created and has full access to s3

- S3_POC_AWS_ACCESS_KEY_ID
- S3_POC_AWS_SECRET_ACCESS_KEY

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*", "s3-object-lambda:*"],
      "Resource": "*"
    }
  ]
}
```

## Environment Variable Setup

### Secret Key

Create in IAM within AWS

- S3_POC_AWS_ACCESS_KEY_ID
- S3_POC_AWS_SECRET_ACCESS_KEY

### S3 Locations

- S3_POC_REGION
  - aws region
  - `eu-west-1` (for example)
- S3_POC_PUBLIC && S3_POC_PRIVATE
  - Bucket Name
  - `test-private-1231233`
  - Because region and bucket name provided **don't use** something like this `test-public-1231233.s3.eu-west-1`

## Expected output

If you run the private and public actions

```json
Public link is : https://test-public-12312123.s3.eu-west-111.amazonaws.com/junk_manual.txt
Private link is : https://test-public-12312123.s3.eu-west-111.amazonaws.com/junk_manual.txt
Region is : eu-west-111
AWS Access Key ID: AKRRRRLQUFFF4LRUHOI
File downloaded successfully to Data/Private/downloaded_file_boto.txt
File downloaded successfully to Data/public/downloaded_file.txt
File uploaded successfully to S3 bucket test-public-12312123 with key uploaded_file_pub.txt
File downloaded successfully to Data/Private/downloaded_file_boto.txt
File downloaded successfully to Data/Private/downloaded_file_expect_denied.txt
File uploaded successfully to S3 bucket test-private-12312123 with key uploaded_file_private.txt
```
