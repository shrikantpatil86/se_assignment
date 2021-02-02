"""
xml processing module
"""

import config
from urllib.parse import urlparse
import pandas as pd
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from xml.etree.ElementTree import parse
import config
import boto3
import urllib
import zipfile
import os


os.environ["RESOURCE_NAME"] = "xml_handler"
from app_logger import AppLogger
LOGGER= AppLogger(__name__).get_logger()

class XmlHandler():
    def __init__(self, document_url):
        self.document_url = document_url
        LOGGER.info("Handler initiated")

    def get_document_root(self):
        """Parses xml and returns root element"""
        LOGGER.info("get_document_root")
        root = False
        try:
            doc = urlopen(self.document_url)
            tree = ET.parse(doc)
            root = tree.getroot()
        except Exception as e:
            LOGGER.error(e)
        return root

    def get_download_link(self,root):
        """Searches for element where file_type is equal to 'DLTINS'
           and returns download link of matched element with an assumption that
           all nodes containing file_type has a download link"""
        download_link = False
        file_types = root.findall("./result/doc/str[@name='file_type']")
        download_links = root.findall("./result/doc/str[@name='download_link']")
        dltins_indices = [ index for index,value in enumerate(file_types) if value.text == "DLTINS"]
        if len(dltins_indices) > 0:
            download_link = download_links[dltins_indices[0]].text
        return download_link

    def get_download_file_name(self,download_link):
        "Returns xml file name from download link"
        return urlparse(download_link).path.split('/')[-1].replace(".zip",".xml")

    def download_and_unzip(self,download_url):
        """
        Takes url and returns unzipped folder path after download and unzip operation"

        Reference:https://stackoverflow.com/questions/6861323/download-and-unzip-file-with-python
        """
        LOGGER.info("Download & Unzip operation started")
        download_unzipped = False
        if type(download_url) == str:
            
            zip_path, _ = urllib.request.urlretrieve(download_url)
            with zipfile.ZipFile(zip_path, "r") as f:
                try:
                    f.extractall(config.RESOURCES_PATH)
                    downloaded_path = os.path.join(config.RESOURCES_PATH, self.get_download_file_name(download_url))
                    if os.path.exists(downloaded_path):
                        download_unzipped = downloaded_path
                except Exception as e:
                    LOGGER.error("Exception is {}".format(e))
        else:
            LOGGER.info("URL should be string instead of {}".format(type(download_url)))
        return download_unzipped
        
    def parse_xml(self,file_path):
        """Takes xml file path and returns root element after parsing the file"""
        LOGGER.info("Parsing xml..")
        root = False
        #file_path = "DLTINS_20210117_01of01.xml"
        if os.path.exists(file_path):
            root = ET.parse(file_path).getroot()
        return root

    def get_issuers(self, root):
        """Takes root element and returns Issr list"""
        issuer_values = False
        required_tags = root.findall(
        "{urn:iso:std:iso:20022:tech:xsd:head.003.001.01}Pyld/xmlns:Document/xmlns:FinInstrmRptgRefDataDltaRpt/xmlns:FinInstrm/xmlns:TermntdRcrd/xmlns:Issr", 
        namespaces={'xmlns': 'urn:iso:std:iso:20022:tech:xsd:auth.036.001.02'})
        if len(required_tags) > 0:
            issuer_values = [tag.text for tag in required_tags]
        return issuer_values

    def get_tag_values(self, root, tag_string):
        """Takes root element and tag and returns list of values or False in terms of no match"""
        tag_values = False
        required_tags = root.findall(
        "{urn:iso:std:iso:20022:tech:xsd:head.003.001.01}Pyld/xmlns:Document/xmlns:FinInstrmRptgRefDataDltaRpt/xmlns:FinInstrm/xmlns:TermntdRcrd/xmlns:FinInstrmGnlAttrbts/xmlns:"+tag_string, 
        namespaces={'xmlns': 'urn:iso:std:iso:20022:tech:xsd:auth.036.001.02'})
        if len(required_tags) > 0:
            tag_values = [tag.text for tag in required_tags]
        return tag_values

    def get_csv_data(self, root):
        """Takes root element, extracts and returns data for generating csv
            Assumption:
            1. All the tags need to be present
            2. Length of extracted elements in each tag should match lenght of remaining tags
            """
        payload = False
        ids = self.get_tag_values(root, "Id")
        if ids:
            full_names = self.get_tag_values(root, "FullNm")
            if full_names:
                clss = self.get_tag_values(root, "ClssfctnTp")
                if clss:
                    commodities = self.get_tag_values(root, "CmmdtyDerivInd")
                    if commodities:
                        currencies = self.get_tag_values(root, "NtnlCcy")
                        if currencies:
                            issuers = self.get_issuers(root)
                            if issuers:
                                equal_length = ( len(ids) == len(full_names) and
                                                 len(clss) == len(commodities) and
                                                 len(currencies) == len(issuers)
                                                )
                                if equal_length:
                                    payload = {
                                            "FinInstrmGnlAttrbts.Id" : ids,
                                            "FinInstrmGnlAttrbts.FullNm": full_names,
                                            "FinInstrmGnlAttrbts.ClssfctnTp": clss,
                                            "FinInstrmGnlAttrbts.CmmdtyDerivInd":commodities,
                                            "FinInstrmGnlAttrbts.NtnlCcy":currencies,
                                            "Issr":issuers
                                            }
                                else:
                                    LOGGER.info("Problem with data size")
                        else:
                            LOGGER.info("Problem with Currency")
                    else:
                        LOGGER.info("Problem with commodities")
                else:
                    LOGGER.info("Problem with clss")
            else:
                LOGGER.info("Problem with full name")
        else:
            LOGGER.info("Problem with IDs")
        return payload

    def generate_csv(self, payload):
        csv_generated = False
        if type(payload) == dict:
            LOGGER.info("Starting csv generation process")
            df = pd.DataFrame(payload)
            df = df[config.CSV_COLUMN_NAMES] #Align the columns
            try:
                LOGGER.info("Exporting CSV")
                df.to_csv(config.CSV_EXPORT_NAME, encoding="utf-8", index=False)
                csv_generated = True
            except Exception as e:
                LOGGER.error(e)
        else:
            LOGGER.info("Payload must be a dictionary instead of {}".format(type(payload)))
        return csv_generated

	
	