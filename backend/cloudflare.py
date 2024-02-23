# cloudflare related config

from requests import get, patch
from requests.exceptions import HTTPError
from json import load

class Cflr_API:

    def __init__(self):

        # configuration status 

        self.cflr_api_configured = None

        # authentication
        self.cflr_email_address = None
        self.cflr_api_key = None

        # fqdn-related config
        self.cflr_api_zone_id = None
        self.cflr_fqdn_name = None

        # ip address info

        self.current_ip = None
        self.cflr_record_id = None
        self.cflr_current_ttl = None
        self.cflr_proxied = None


    def get_config(self, config_file):
        """
        Read configuration file and set API credentials to interact with Cloudflare.
        """

        try:
            with open(config_file, 'r') as cfg_file:

                cfg = load(cfg_file)
                cflr_cfg = cfg['cflr']

                self.cflr_email_address = cflr_cfg['cflr_email_address']
                self.cflr_api_key = cflr_cfg['cflr_api_key']
                self.cflr_api_zone_id = cflr_cfg['cflr_zone_id']
                self.cflr_fqdn_name = cflr_cfg['cflr_fqdn_name']
                print("CloudFlare is configured")

                self.cflr_api_configured = True
        
        except (KeyError, ValueError) as error:
            print(f'Error processing config file {config_file} ended with error: {error}')
            print(f'Skipping CloudFlare...')
            self.cflr_api_configured = False

    def get_current_ip(self):
        """
        Read current value of IP address from the CloudFlare's API
        """
        # set API configurables

        api_url = f'https://api.cloudflare.com/client/v4/zones/{self.cflr_api_zone_id}/dns_records'

        api_headers = {
            'Authorization': f'Bearer {self.cflr_api_key}',
            'Content-Type': 'application/json'
        }

        try:
            response = get(url=api_url, headers=api_headers)

            if response.status_code == 200:

                # loop through the result
                for record in response.json()['result']:
                    
                    # if name matches config - set variables
                    if record['name'] == self.cflr_fqdn_name:
                        try:
                            self.cflr_record_id = record['id']
                            self.current_ip = record['content']
                            self.cflr_current_ttl = record['ttl']
                            self.cflr_proxied = record['proxied']
                        
                        except KeyError as error:

                            print(f'Finished with an error: {error}')

            else:
                raise HTTPError
                
        except HTTPError as error:
            print(f'Unable to extract data: {error}')


    def set_new_ip(self, new_ip):
        """
        Map FQDN to the current IP address 
        """
        
        api_url = f'https://api.cloudflare.com/client/v4/zones/{self.cflr_api_zone_id}/dns_records/{self.cflr_record_id}'

        api_headers = {
            'Authorization': f'Bearer {self.cflr_api_key}'
        }

        api_payload = {
            'content': new_ip,
            'ttl' : self.cflr_current_ttl,
            'proxied': self.cflr_proxied 
        }

        try:
            response = patch(url=api_url, headers=api_headers, json=api_payload)

            if response.status_code == 200:
                print(f'New record for {self.cflr_fqdn_name} is set to {new_ip}')
            
            else:
                raise HTTPError

        except HTTPError as error:
            print(f'Failed to set new IP: {error}')
            

# test area

if __name__ == '__main__':

    cflr_api = Cflr_API()
    cflr_api.get_config(config_file='.config.json')
    cflr_api.get_current_ip()
    cflr_api.set_new_ip(new_ip='124.124.124.124')
    print(cflr_api.cflr_api_configured, cflr_api.current_ip, cflr_api.cflr_record_id, cflr_api.cflr_proxied, cflr_api.cflr_current_ttl)