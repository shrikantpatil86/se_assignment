"""
AWS utilities module
Inspired by https://www.gormanalysis.com/blog/connecting-to-aws-s3-with-python/
"""

import boto3
import os
import sys
import config

os.environ["RESOURCE_NAME"] = "aws_utils"
from app_logger import AppLogger
LOGGER= AppLogger(__name__).get_logger()

class AwsUtils():

    def get_s3_resource(self):
        """Initializes and returns s3 resource"""
        s3 = boto3.resource(
            service_name='s3',
            region_name=config.AWS_REGION_NAME,
            aws_access_key_id=config.AWS_ACCESS_ID,
            aws_secret_access_key=config.AWS_SECRET
        )
        LOGGER.info("returning s3")
        return s3

    def upload_csv_to_s3(self):
        """Upload file to s3"""
        uploaded = False
        s3 = self.get_s3_resource()
        try:
            s3.Bucket(config.AWS_BUCKET_NAME).upload_file(Filename=config.CSV_EXPORT_NAME, Key='upload.csv')
            uploaded = True
        except Exception as e:
            print(e)
        return uploaded