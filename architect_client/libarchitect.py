
import os
import yaml
import json

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse


def load_yaml_file(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def write_json_file(path, content):
    file_handler = open(path, "w")
    json.dump(content, file_handler)
    file_handler.close()


class ArchitectException(Exception):
    pass


class ArchitectClient(object):

    def __init__(self, api_url=None, project=None):
        if api_url is None:
            config = load_yaml_file('/etc/architect/client.yml')
            self.api_url = 'http://{}:{}'.format(config['host'],
                                                 config['port'])
            self.project = config.get('project', 'default')
            self.project_mapping = config.get('project_mapping', {})
        else:
            self.api_url = api_url
            self.project = project
            self.project_mapping = {}

    def _req_get(self, path):
        '''
        A thin wrapper to get http method of architect api
        print(api._req_get('/keys'))
        '''
        import requests

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        # self._ssl_verify = self.ignore_ssl_errors
        params = {'url': self._construct_url(path),
                  'headers': headers}
        try:
            resp = requests.get(**params)
            if resp.status_code == 401:
                raise ArchitectException(str(resp.status_code) + ':Authentication denied')
                return
            if resp.status_code == 500:
                raise ArchitectException('{}: Server error.'.format(resp.status_code))
                return
            if resp.status_code == 404:
                raise ArchitectException(str(resp.status_code) +' :This request returns nothing.')
                return
        except ArchitectException as e:
            print(e)
            return
        return resp.json()

    def _req_post_json(self, path, data):
        '''
        A thin wrapper to postt http method of architect api
        print(api._req_post('/keys'))
        '''
        import requests

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        # self._ssl_verify = self.ignore_ssl_errors
        params = {'url': self._construct_url(path),
                  'headers': headers,
                  'json': data}
        try:
            resp = requests.post(**params)
            if resp.status_code == 401:
                raise ArchitectException(str(resp.status_code) + ':Authentication denied')
                return
            if resp.status_code == 500:
                raise ArchitectException('{}: Server error.'.format(resp.status_code))
                return
            if resp.status_code == 404:
                raise ArchitectException(str(resp.status_code) +' :This request returns nothing.')
                return
        except ArchitectException as e:
            print(e)
            return
        return resp.json()

    def _construct_url(self, path):
        '''
        Args:
            path: the path to the architect-api resource
        '''

        relative_path = path.lstrip('/')
        return urlparse.urljoin(self.api_url, relative_path)

    def create_inventory(self, cluster_name, domain_name):
        path = '/inventory/v1/inventory-create/data.json'
        data = {
            'inventory_name': self.project,
            'cluster_name': cluster_name,
            'domain_name': domain_name
        }
        return self._req_post_json(path, data)

    def create_manager(self, name, url, user, password):
        path = '/manager/v1/manager-create/data.json'
        data = {
            'manager_name': name,
            'manager_url': url,
            'manager_user': user,
            'manager_password': password
        }
        return self._req_post_json(path, data)

    def push_node_info(self, data):
        path = "/salt/v1/minion/{}".format(self.project)
        return self._req_post_json(path, data)

    def push_event(self, data):
        path = "/salt/v1/event/{}".format(self.project)
        return self._req_post_json(path, data)

    def classify_node(self, data):
        path = "/salt/v1/class/{}".format(self.project)
        return self._req_post_json(path, data)

    def get_data(self, source, resource=None):
        if resource is None:
            path = '/inventory/v1/{}/data.json?source={}'.format(self.project,
                                                                 source)
        else:
            domain = '.'.join(resource.split('.')[1:])
            if domain in self.project_mapping:
                project = self.project_mapping[domain]
            else:
                project = self.project

            path = '/inventory/v1/{}/{}/data.json?source={}'.format(project,
                                                                    resource,
                                                                    source)
        return self._req_get(path)
