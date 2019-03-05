'''
GCMD JSON
Converts GCMD files into JSON
'''

# Import necessary libraries
import requests
import json
from io import BytesIO
from lxml import etree


class gcmdFile(dict):

    def __init__(self, rdf_url):
        self.url = rdf_url
        self.tree = self._import()
        
        self._mutable = True
        self._build_dict()
        self._mutable = False

    def _import(self):
        response = requests.get(self.url, headers={'Connection': 'close'})
        rdf_file = BytesIO(response.content)
        tree = etree.parse(rdf_file)  # could fail for a lot of reasons
        return tree

    def save(self, json_path='gcmd.json'):
        with open(json_path, 'w') as outfile:
            json.dump(self, outfile)

    def _build_dict(self):

        for top in self.tree.findall('*'):

            short_name = None
            for element in top.findall('{http://www.w3.org/2004/02/skos/core#}prefLabel'):
                short_name = element.text
                self[short_name] = {'short_name': short_name}

            if short_name:
                for element in top.findall('{http://gcmd.gsfc.nasa.gov/kms#}altLabel'):
                    long_name = element.attrib['{http://gcmd.gsfc.nasa.gov/kms#}text']
                    self[short_name].update({'long_name': long_name})

                for element in top.findall('{http://www.w3.org/2004/02/skos/core#}definition'):
                    description = element.text
                    self[short_name].update({'description': description})

    def __setitem__(self, key, value):
        if self._mutable:
            super(gcmdFile, self).__setitem__(key, value)
        else:
            raise ZeroDivisionError('To add keywords, please contact GCMD directly.')

    def __delitem__(self, key, value):
        if self._mutable:
            super(gcmdFile, self).__setitem__(key, value)
        else:
            raise ZeroDivisionError('To remove keywords, please contact GCMD directly.')