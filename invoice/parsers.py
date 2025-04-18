import xml.etree.ElementTree as ET
from rest_framework.parsers import BaseParser

class XMLParser(BaseParser):
    media_type = 'application/xml'

    def parse(self, stream, media_type=None, parser_context=None):
        tree = ET.parse(stream)
        root = tree.getroot()
        # Assuming the structure of XML data is <notif><transaction>...</transaction></notif>
        transaction = root.find('transaction')
        if transaction is not None:
            return self._xml_to_dict(transaction)
        return {}

    def _xml_to_dict(self, root):
        result = {}
        for child in root:
            if len(child) > 0:
                result[child.tag] = self._xml_to_dict(child)
            else:
                tag = child.tag
                if tag == 'posteddate':
                    tag = 'posted_date'
                elif tag == 'statementdate':
                    tag = 'statement_date'
                result[tag] = child.text
        return result
