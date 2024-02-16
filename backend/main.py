from aws import AWS_API
from ip_handler import My_IP

### functions

def verify_address(old_ip, new_ip):

    if old_ip == new_ip:
        return True
    else:
        return False


### main code

my_ip = My_IP()

aws_api = AWS_API()
aws_api.get_config(config_file='.config.json')
aws_api.aws_get_current_ip()

validation_status = verify_address(old_ip=aws_api.current_ip, new_ip=my_ip.current_ip)

if not validation_status:
    aws_api.aws_set_new_ip(new_ip=my_ip.current_ip)
else:
    print(f'Addresses are the same, no need to update!')