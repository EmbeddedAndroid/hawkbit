import argparse
import requests
import json

__version__ = 1.0

user = 'admin'
password  = 'admin'

def publish(provider, name, type, version, description, artifact,
            hostname, ds_url=None, sm_url=None):
    # Publish Software Module
    headers = { 'Content-Type': 'application/hal+json;charset=UTF-8',
                'Accept': 'application/hal+json' }
    sm = { 'requiredMigrationStep': False,
           'vendor': provider,
           'name': name,
           'type': type,
           'description': description,
           'version': version }
    if ds_url is None:
        ds_url = 'http://%s:8080/rest/v1/distributionsets' % hostname
    if sm_url is None:
        sm_url = 'http://%s:8080/rest/v1/softwaremodules' % hostname
    response = requests.post(sm_url, data=json.dumps([sm]), auth=(user, password), headers=headers)
    if response.status_code != 500:
        data = json.loads(response.content)
        print data
        for item in  json.loads(response.content):
            if 'id' in item:
                id = item['id']
            if '_links' in item:
                if 'artifacts' in item['_links']:
                    artifacts_url = item['_links']['artifacts']['href']
                if 'self' in item['_links']:
                    self_url = item['_links']['self']['href']
                if 'type' in item['_links']:
                    type_url = item['_links']['type']['href']
                if 'metadata' in item['_links']:
                    metadata_url = item['_links']['metadata']['href']
        print artifacts_url
        print self_url
        print type_url
        print metadata_url
        print id
    # Upload Artifact
    headers = {'Accept': 'application/json' }
    artifacts = {'file': open(artifact, 'rb')}
    response = requests.post(artifacts_url, auth=(user, password), headers=headers, files=artifacts)
    if response.status_code != 500:
        headers = { 'Content-Type': 'application/json',
                    'Accept': 'application/json' }
        ds = { 'requiredMigrationStep': False,
               'vendor': provider,
               'name': name,
               'type': type,
               'description': description,
               'version': version,
               'modules': [{'id': id}],
               '_links': {'artifacts': artifacts_url,
                          'self': self_url,
                          'type': type_url,
                          'metadata': metadata_url} }
        response = requests.post(ds_url, data=json.dumps([ds]), auth=(user, password), headers=headers)
        if response.status_code != 500:
            print response.content




def main():
    description = 'Simple Hawkbit API Wrapper for publishing artifacts'
    parser = argparse.ArgumentParser(version=__version__, description=description)
    parser.add_argument('-p', '--provider', help='SW Module Provider', required=True)
    parser.add_argument('-n', '--name', help='Name', required=True)
    parser.add_argument('-t', '--type', help='Name', required=True)
    parser.add_argument('-sv', '--swversion', help='Version', required=True)
    parser.add_argument('-d', '--description', help='Version', required=True)
    parser.add_argument('-f', '--file', help='Version', required=True)
    parser.add_argument('-ds', '--distribution-sets',
                        help='Distribution Sets URL')
    parser.add_argument('-sm', '--software-modules',
                        help='Software Modules URL')
    parser.add_argument('-host', '--hostname', help='Hawkbit Server Hostname or IP', default='hawkbit')
    args = parser.parse_args()
    publish(args.provider, args.name, args.type, args.swversion,
            args.description, args.file, args.hostname, args.distribution_sets,
            args.software_modules)

if __name__ == '__main__':
    main()
