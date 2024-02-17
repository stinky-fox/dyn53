# this is a collection of functions and classes used to handle IP-data

from requests import get
from datetime import datetime
from boto3 import client

class My_IP:

    def __init__(self):

        self.current_ip = None
        self.last_checked = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())          



    def get_ip(self):

        url = 'https://ip.me'

        response = get(url=url)

        if response.status_code == 200:
             self.current_ip = response.content.decode('utf-8').split('\n')[0]
        else:
            print(f"Error checking IP, error code")


# test area

if __name__ == '__main__':
    my_ip = My_IP()
    my_ip.get_ip()

    print(my_ip.ip_addr)