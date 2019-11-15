import boto3
import botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET
import time

# sending your keys to AWS, so that you can upload your picture to aws server
s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


# acl = access control list
def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
        return file.filename

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return False  # e


# making each profile_image unique by adding the current time in seconds from epoch
def unique_filename(file):
    return str(int(time.time())) + file.filename
