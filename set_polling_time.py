import argparse
import requests
import json
import time

__version__ = 1.0

user = 'admin'
password  = 'admin'


def set(time, hostname):
    headers = { 'Content-Type': 'application/hal+json;charset=UTF-8',
                'Accept': 'application/hal+json' }
    config = { 'keyName': 'pollingTime',
               'value': time }
    config_url = 'http://%s:8080/rest/v1/system/configs/pollingTime' % hostname
    response = requests.put(config_url, data=json.dumps(config), auth=(user, password), headers=headers)
    if response.status_code != 500:
        data = json.loads(response.content)
        print data

def main():
    description = 'Simple Hawkbit API Wrapper for setting the polling time'
    parser = argparse.ArgumentParser(version=__version__, description=description)
    parser.add_argument('-t', '--time', help='Polling time to set, HH:MM:SS notation', required=True)
    parser.add_argument('-host', '--hostname', help='Hawkbit Server Hostname or IP', default='hawkbit')
    args = parser.parse_args()
    set(args.time, args.hostname)

if __name__ == '__main__':
    main()
