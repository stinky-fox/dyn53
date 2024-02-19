from os import environ, path
from time import sleep
from json import load
from aws import AWS_API
from ip_handler import My_IP
from datetime import datetime

### global default vars

EXIT_TIMEOUT = 120
DEFAULT_CONFIG_FILE = '.config.json'

### functions

def verify_address(old_ip, new_ip):

    if old_ip == new_ip:
        return True
    else:
        return False

def sysconfig_loader(config_file):

    timeout = 300
    try:
        with open(config_file, 'r') as cfg:
            config = load(cfg)
            timeout = config['system']['timeout']

    except (FileNotFoundError, ValueError) as error:
        # if error - return default to 5m (300s)
        print(f'Opening config file had errored out with an error: {error}')
    
    finally:
        return timeout

def config_file_resolver():

    try:
        config_file = environ['CONFIG_FILE']
        if path.isfile(config_file):
            return config_file
        else:
            raise FileNotFoundError

    except (KeyError, FileNotFoundError):
        config_file = DEFAULT_CONFIG_FILE
        print(f"Config file is not defined, falling back to defaults {config_file}")
        if path.isfile(config_file):
            return config_file
        else:
            return False

### main code

config_file = config_file_resolver()

if not config_file:
    print(f"Failed to locate configuration file, exiting in {EXIT_TIMEOUT} seconds")
    sleep(EXIT_TIMEOUT)
    exit(1)

else:
    my_ip = My_IP()
    aws_api = AWS_API()
    aws_api.get_config(config_file=config_file)
    timeout = sysconfig_loader(config_file=config_file)

    counter = 0

    if aws_api.aws_api_configured:
        while True:

            if counter != 0:
                sleep(timeout)

            my_ip.get_ip()
            aws_api.aws_get_current_ip()

            validation_status = verify_address(old_ip=aws_api.current_ip, new_ip=my_ip.current_ip)

            dtnow = datetime.now()
            if not validation_status:
                print(f'{dtnow} : Addreses are different. Changing to {my_ip.current_ip}')
                aws_api.aws_set_new_ip(new_ip=my_ip.current_ip)
            else:
                print(f'{dtnow} : Addresses are the same, no need to update!')
            
            counter+=1
    else: 
        print(f'AWS API not configured, exiting in {EXIT_TIMEOUT} seconds')
        sleep(EXIT_TIMEOUT)
        exit(1)