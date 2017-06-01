import argparse
import requests
import json

__version__ = 1.0

user = 'admin'
password  = 'admin'


def rollout(name, targetfilter, groups, id, hostname, start=False):
    # Create the Rollout
    headers = { 'Content-Type': 'application/hal+json;charset=UTF-8',
                'Accept': 'application/hal+json' }
    rollout = { 'name': name,
                'targetFilterQuery': targetfilter,
                'amountGroups': groups,
                'distributionSetId': id }
    rollout_url = 'http://%s:8080/rest/v1/rollouts' % hostname
    response = requests.post(rollout_url, data=json.dumps(rollout), auth=(user, password), headers=headers)
    if response.status_code != 500:
        data = json.loads(response.content)
        print data
        for key in data:
            if 'id' == key:
                rollout_id = data[key]
            if '_links' == key:
                if 'start' in data[key]:
                    start_url = data[key]['start']['href']
                if 'self' in data[key]:
                    self_url = data[key]['self']['href']
                if 'resume' in data[key]:
                    resume_url = data[key]['resume']['href']
                if 'pause' in data[key]:
                    pause_url = data[key]['pause']['href']
                if 'groups' in data[key]:
                    groups_url = data[key]['pause']['href']
        print start_url
        print self_url
        print resume_url
        print pause_url
        print groups_url
        print rollout_id

    # Start the rollout
    if start:
        run = True
        print "Waiting for rollout to be ready..."
        while run:
            response = requests.get(self_url, auth=(user, password), headers=headers)
            if response.status_code != 500:
                data = json.loads(response.content)
                for key in data:
                    if 'status' == key:
                        if 'ready' == data[key]:
                            run = False
        response = requests.post(start_url, auth=(user, password), headers=headers)
        if response.status_code != 500:
            print "Rollout Started"

def main():
    description = 'Simple Hawkbit API Wrapper for creating rollouts'
    parser = argparse.ArgumentParser(version=__version__, description=description)
    parser.add_argument('-n', '--name', help='Rollout Name', required=True)
    parser.add_argument('-t', '--targetfilter', help='Rollout Target Filter Query', required=True)
    parser.add_argument('-g', '--groups', help='Number of Rollout Groups', type=int, required=True)
    parser.add_argument('-i', '--id', help='Distribution Set ID', type=int, required=True)
    parser.add_argument('-s', '--start', help='Starts the rollout after creating it', action="store_true")
    parser.add_argument('-host', '--hostname', help='Hawkbit Server Hostname or IP', default='hawkbit')
    args = parser.parse_args()
    rollout(args.name, args.targetfilter, args.groups,
            args.id, args.hostname, args.start)

if __name__ == '__main__':
    main()
