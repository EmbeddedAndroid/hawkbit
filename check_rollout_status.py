import argparse
import requests
import json
import time

__version__ = 1.0

user = 'admin'
password  = 'admin'


def rollout(id, hostname, xfail=False):
    headers = { 'Content-Type': 'application/hal+json;charset=UTF-8',
                'Accept': 'application/hal+json' }
    rollout_url = 'http://%s:8080/rest/v1/rollouts/%s' % (hostname, id)
    response = requests.get(rollout_url, auth=(user, password), headers=headers)
    if response.status_code != 500:
        data = json.loads(response.content)
        print data
        for key in data:
            if 'totalTargets' == key:
                total_targets = data[key]
            if 'totalTargetsPerStatus' == key:
                target_error_count = data[key]['error']
                target_success_count = data[key]['finished']

        if total_targets == target_error_count:
            if xfail:
                print "Rollout failed with errors, but this was expected."
                exit(0)
            else:
                print "Rollout failed with errors."
                exit(1)
        elif total_targets == target_success_count:
            if xfail:
                print "Rollout succeeded with no errors, this was unexpected."
                exit(1)
            else:
                print "Rollout succeeded with no errors."
                exit(0)
        else:
            print "Rollout failed with a subset of errors."
            exit(1)

def main():
    description = 'Simple Hawkbit API Wrapper for checking rollout status'
    parser = argparse.ArgumentParser(version=__version__, description=description)
    parser.add_argument('-i', '--id', help='Rollout ID', type=int, required=True)
    parser.add_argument('-x', '--xfail', help='Inverts the return code if a failure is expected', action="store_true")
    parser.add_argument('-host', '--hostname', help='Hawkbit Server Hostname or IP', default='hawkbit')
    args = parser.parse_args()
    rollout(args.id, args.hostname, args.xfail)

if __name__ == '__main__':
    main()
