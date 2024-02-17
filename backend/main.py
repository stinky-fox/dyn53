from time import sleep
from json import load
from aws import AWS_API
from ip_handler import My_IP
from datetime import datetime

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
            
### main code

timeout = sysconfig_loader(config_file='.config.json')

my_ip = My_IP()
my_ip.get_ip()

print(my_ip.current_ip)

aws_api = AWS_API()

aws_api.get_config(config_file='.config.json')

counter = 0

while True:

    if counter != 0:
        sleep(timeout)

    aws_api.aws_get_current_ip()

    validation_status = verify_address(old_ip=aws_api.current_ip, new_ip=my_ip.current_ip)

    dtnow = datetime.now()
    if not validation_status:
        print(f'{dtnow} : Addreses are different. Changing to {my_ip.current_ip}')
        aws_api.aws_set_new_ip(new_ip=my_ip.current_ip)
    else:
        print(f'{dtnow} : Addresses are the same, no need to update!')
    
    counter+=1
