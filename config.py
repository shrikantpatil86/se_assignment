LOG_LEVEL = 10
LOG_DIR = "logs"

DOCUMENT_URL = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"

RESOURCES_PATH = "resources"
XMLNS_1 = "urn:iso:std:iso:20022:tech:xsd:head.003.001.01"
XMLNS_2 = "urn:iso:std:iso:20022:tech:xsd:auth.036.001.02"
CSV_COLUMN_NAMES = ["FinInstrmGnlAttrbts.Id", "FinInstrmGnlAttrbts.FullNm", "FinInstrmGnlAttrbts.ClssfctnTp", "FinInstrmGnlAttrbts.CmmdtyDerivInd", "FinInstrmGnlAttrbts.NtnlCcy",
"Issr"]
CSV_EXPORT_NAME = "upload.csv"

AWS_USER = "steeluser"
AWS_BUCKET_NAME = "steelresources"
AWS_REGION_NAME = "us-east-2"
AWS_S3_BUCKET = "steelbucket"
AWS_ACCESS_ID = "###"
AWS_SECRET = "###/###"


