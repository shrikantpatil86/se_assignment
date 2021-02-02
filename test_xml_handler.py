import unittest
import config
from xml_handler import XmlHandler

class Testing(unittest.TestCase):
    def test_generate_csv(self):
        x_obj = XmlHandler(config.DOCUMENT_URL)
        data = [1, 2, 3]
        result = x_obj.generate_csv(payload=data)
        self.assertEqual(result, False)

    def test_download_and_unzip(self):
        x_obj = XmlHandler(config.DOCUMENT_URL)
        data = [1, 2, 3]
        result = x_obj.download_and_unzip(data)
        self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()