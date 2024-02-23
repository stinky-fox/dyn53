from sys import exit
from time import sleep
from datetime import datetime
from ip_handler import My_IP
from aws import AWS_API
from cloudflare import Cflr_API
from misc import verify_address, sysconfig_loader, config_file_resolver, service_discoverer

### global default vars

EXIT_TIMEOUT = 120
DEFAULT_CONFIG_FILE = '.config.json'


############################ main code ##########################################

try:
    config_file = config_file_resolver(default_config_file=DEFAULT_CONFIG_FILE)

    services = service_discoverer(config_file=config_file)
    print('Configured services: ', *(services))

    timeout = sysconfig_loader(config_file=config_file)
    print('Configured timeout: ', timeout, 'seconds')

except FileNotFoundError as error:
    print(f"Failed to locate configuration file, exiting in {EXIT_TIMEOUT} seconds")
    sleep(EXIT_TIMEOUT)
    exit(1)

# configure services
dns_provider = {}

for index, service in enumerate(services):
    if service == 'aws':
        dns_provider[service] = AWS_API()
        dns_provider[service].get_config(config_file=config_file)

        if not dns_provider[service].aws_api_configured:
            services.pop()[index]

    elif service == 'cflr':
        dns_provider[service] = Cflr_API()
        dns_provider[service].get_config(config_file=config_file)

        if not dns_provider[service].cflr_api_configured:
            services.pop()[index]


# check if any service configured, otherwise terminate
if len(services) > 0:
    my_ip = My_IP()
    counter = 0

    # start configuration loop
    while True:

        if counter != 0:
            sleep(timeout)
        
        my_ip.get_ip()

        for service in services: 
            
            dns_provider[service].get_current_ip()
            validation_status = verify_address(old_ip=dns_provider[service].current_ip, new_ip=my_ip.current_ip)
            dtnow = datetime.now()

            if not validation_status:
                print(f'{dtnow} : Addreses are different. Changing to {my_ip.current_ip}')
                dns_provider[service].set_new_ip(new_ip=my_ip.current_ip)
            else:
                print(f'{dtnow} : Addresses are the same, no need to update!')
            
        counter+=1
else: 
    print(f'No service is configured, exiting in {EXIT_TIMEOUT} seconds')
    sleep(EXIT_TIMEOUT)
    exit(1)