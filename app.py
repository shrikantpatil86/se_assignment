import pandas as pd
import xml.etree.ElementTree as ET
import config
import boto3
from xml_handler import XmlHandler
from aws_utils import AwsUtils
import os
import sys
import datetime

os.environ["RESOURCE_NAME"] = "app_run"
from app_logger import AppLogger
LOGGER= AppLogger(__name__).get_logger()

if __name__ == "__main__":
    script_start_time = datetime.datetime.now()
    c_aws = AwsUtils()
    c_xml = XmlHandler(config.DOCUMENT_URL)
    try:
        root = c_xml.get_document_root()
        download_link = c_xml.get_download_link(root)
        download_and_unzip = c_xml.download_and_unzip(download_link)
        parsed = c_xml.parse_xml(download_and_unzip)
        csv_data = c_xml.get_csv_data(parsed)
        csv_generated = c_xml.generate_csv(csv_data)
        if csv_generated:
            s3_upload = c_aws.upload_csv_to_s3()
            if s3_upload:
                LOGGER.info("Successfully uploaded csv file")
                LOGGER.info("Total time taken by program is {}".format(datetime.datetime.now() - script_start_time))
    except Exception as e:
        LOGGER.error(e)
    
