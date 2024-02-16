###############################################
#  Contains AWS-related Classes and functions #
###############################################


## import libs
from json import load 
from os import environ
from sys import exit
from boto3 import client

# define classes
class AWS_API:

    def __init__(self):

        # aws api authentication settings
        self.aws_access_key = None
        self.aws_secret_key = None
        self.aws_default_region = 'us-east-1'

        # aws Route 53 data 
        self.aws_r53_zone_id = None
        self.aws_r53_name = None

        # aws route 53 specific Record's data
        self.current_ip = None
        self.current_ttl = None

    # Get config function
    def get_config(self, **kwargs):
        """
        Set AWS configuration
        """
        
        # define sub functions

        def process_envs():
            """
            Used as a backup function when configuration file is missing. Takes config from environment variables
            """
            try:
                self.aws_access_key = environ['AWS_ACCESS_KEY']
                self.aws_secret_key = environ['AWS_SECRET_KEY']
                self.aws_r53_zone_id = environ['AWS_R53_ZONE_ID']
                self.aws_r53_name = environ['AWS_R53_NAME']
                result = True

            except KeyError as error:
                print(f'Unable to extract {error} from the env variables. Not defined!')
                result = False
            
            finally:
                return result

        def read_cfg_file(config_file):
            """
            Open configuration JSON file and look for AWS-related configuration. 
            """
            try:
                with open(config_file, 'r') as cfg_file:
                    cfg = load(cfg_file)
                    aws_cfg = cfg['aws']
                    self.aws_access_key = aws_cfg['aws_access_key']
                    self.aws_secret_key = aws_cfg['aws_secret_key']
                    self.aws_r53_zone_id = aws_cfg['aws_r53_zone_id']
                    self.aws_r53_name = str(aws_cfg['aws_r53_name'] + '.')
                    result = True

                    
            except (FileNotFoundError, ValueError) as error:
                print(f'Processing of {kwargs["config_file"]} ended up with: {error}')
                result = False
    
            finally:
                return result

        # call functions

        if 'config_file' in kwargs:
            print(f'Trying to use {kwargs["config_file"]} first')
            result_file = read_cfg_file(kwargs['config_file'])

            if not result_file:
                print(f'Configuration file result is {result_file}. Trying envs')
                result_env = process_envs()
        else:
            result_file = False
            result_env = process_envs
        
        if not result_file and not result_env:
            print('Skipping AWS confugration...')
        else:
            print("AWS R53 configured")

    # Read current record function
    def aws_get_current_ip(self, **kwargs):
        """
        Function receives current value of the R53 record and sets it as self.current_ip value
        """
        try:
            awsConnector = client('route53', region_name=self.aws_default_region, aws_access_key_id=self.aws_access_key, aws_secret_access_key=self.aws_secret_key)

            list_dns_names = awsConnector.list_resource_record_sets(HostedZoneId=self.aws_r53_zone_id)

            for dns_name in list_dns_names['ResourceRecordSets']:
                if dns_name['Name'] == self.aws_r53_name:
                    try:
                        self.current_ip = dns_name['ResourceRecords'][0]['Value']
                        self.current_ttl = dns_name['TTL']
                    except KeyError as error: 
                        print(f'{error} is missing, please verify if {self.aws_r53_name} is the right DNS name or you are using the correct Zone ID({self.aws_r53_zone_id})!' )   
        
        except Exception as e:
            print(e)

        
    # Update record with new data
    def aws_set_new_ip(self, new_ip):
        """
        Function to supply record with the new IP addr.
        """

        change_data = {
            'Comment': 'Updated using dynr53',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': self.aws_r53_name,
                        'Type': 'A',
                        'TTL': self.current_ttl,
                        'ResourceRecords': [
                            {
                                'Value': new_ip
                            },
                        ],
                    }
                },
            ]
        }

        try:
            awsConnector = client('route53', region_name=self.aws_default_region, aws_access_key_id=self.aws_access_key, aws_secret_access_key=self.aws_secret_key)

            set_record_response = awsConnector.change_resource_record_sets(HostedZoneId=self.aws_r53_zone_id, ChangeBatch=change_data)

            print(f'New record for {self.aws_r53_name} is set to {new_ip}')
        except Exception as e:
            print(e)


#### test code

if __name__ == '__main__':

    aws_api = AWS_API()
    aws_api.get_config(config_file='.config.json')
    aws_api.aws_get_current_ip()
    aws_api.aws_set_new_ip(new_ip='123.123.123.123')

