import argparse
import requests
import json
import time

__version__ = 1.0

user = 'admin'
password  = 'admin'


def poll(targets, hostname):
    headers = { 'Content-Type': 'application/hal+json;charset=UTF-8',
                'Accept': 'application/hal+json' }
    targets_url = 'http://%s:8080/rest/v1/targets' % hostname
    run = True
    while run:
        try:
            response = requests.get(targets_url, auth=(user, password), headers=headers)
            if response.status_code != 500:
                data = json.loads(response.content)
                print data
                for key in data:
                    if 'total' == key:
                        if targets == data[key]:
                            run = False
                            print "Matched number of targets"
            if run:
                time.sleep(5)
        except:
            time.sleep(5)

def main():
    description = 'Simple Hawkbit API Wrapper for waiting for targets to connect'
    parser = argparse.ArgumentParser(version=__version__, description=description)
    parser.add_argument('-t', '--targets', help='Number of Hawkbit Targets to wait for', type=int, required=True)
    parser.add_argument('-host', '--hostname', help='Hawkbit Server Hostname or IP', default='hawkbit')
    args = parser.parse_args()
    poll(args.targets, args.hostname)

if __name__ == '__main__':
    main()
