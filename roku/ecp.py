import requests
import xmltodict
import json

class ECP():
    def __init__(self, ip):
        self.roku_ip = ip
        self.roku_port = 8060
        self.base_url = 'http://{}:{}'.format(self.roku_ip, self.roku_port)

        # Ignoring SSL errors on api.dcx.rackspace.com
        requests.packages.urllib3.disable_warnings()

    def query_apps(self):
        '''
        Method to pull all installed apps on the Roku

        GET /query/apps
        '''

        url = self.base_url + '/query/apps'

        response = requests.get(url)

        response.raise_for_status()

        data = json.dumps(xmltodict.parse(response.text))

        return data
