# misc function set

from os import environ, path
from json import load

def verify_address(old_ip, new_ip):

    if old_ip == new_ip:
        return True
    else:
        return False

def sysconfig_loader(config_file):
    """
    Read configuration file and extract timeout setting between consecutive checks. If not defined - fall back to default 300s
    """
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

def config_file_resolver(default_config_file):
    """
    Check if custom config file name is supplied & file exists, otherwise fall back to default and check if default config file exists. exit if not!
    """

    try:
        config_file = environ['CONFIG_FILE']
        if path.isfile(config_file):
            return config_file
        else:
            raise FileNotFoundError

    except (KeyError,FileNotFoundError):
        config_file = default_config_file
        print(f"Config file is not defined, falling back to defaults {config_file}")
        if path.isfile(config_file):
            return config_file
        else:
            raise FileNotFoundError


def service_discoverer(config_file):
    """
    Discover configured services in the config file
    """
    with open(config_file, 'r') as file:
        cfg = load(file)

    services = []

    for service in cfg.keys():
        if service != 'system':
            services.append(service)

    return services


### test code
if __name__ == '__main__':
    pass
