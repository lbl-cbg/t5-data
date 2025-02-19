import json
import os
import sys
import requests
from requests.auth import HTTPBasicAuth

TARGET_ID_ID = '97'  # the asset attribute id to use for finding the protein target_id
PARENT_NAME_ID = '491'

class JiraConnector:

    DONE_STATE = '41'

    def __init__(self):
        # Connect to Jira
        self.jira_server = os.environ.get('JIRA_HOST', 'https://taskforce5.atlassian.net')
        self.auth = HTTPBasicAuth(os.environ.get('JIRA_USER', 'ajtritt@lbl.gov'), os.environ['JIRA_TOKEN'])
        # Set up headers for the request
        self.workspace_id = self.get("servicedeskapi/assets/workspace")["values"][0]["workspaceId"]
        self.workspace_url = f'https://api.atlassian.com/jsm/assets/workspace/{self.workspace_id}/v1'

    def __get(self, url):
        # Make the request to get the asset details
        headers = {
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, auth=self.auth)
        if response.status_code not in [200, 201, 204]:
            print(f"GET FAIL {url}: {response.status_code} - {response.text}", file=sys.stderr)
            exit(1)
        return response.json()

    def __put(self, url, data):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.put(url, headers=headers, auth=self.auth, data=json.dumps(data))
        if response.status_code not in [200, 201, 204]:
            print(f"PUT FAIL {url}: {response.status_code} - {response.text}", file=sys.stderr)
            exit(1)

        return None if response.status_code == 204 else response.json()

    def __post(self, url, data):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.post(url, headers=headers, auth=self.auth, data=json.dumps(data))
        if response.status_code not in [200, 201, 204]:
            print(f"POST FAIL {url}: {response.status_code} - {response.text}", file=sys.stderr)
            exit(1)

        return None if response.status_code == 204 else response.json()

    def get(self, url):
        url = f'{self.jira_server}/rest/{url}'
        return self.__get(url)

    def put(self, url, data):
        url = f'{self.jira_server}/rest/{url}'
        return self.__put(url, data)

    def post(self, url, data):
        url = f'{self.jira_server}/rest/{url}'
        return self.__post(url, data)

    def create_asset(self, data):
        url = f'{self.workspace_url}/object/create'
        headers = {
                    'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, auth=self.auth, data=json.dumps(data))
        if response.status_code not in [200, 201]:
            print("Failed to create asset:", response.status_code, response.text, file=sys.stderr)
            exit(1)
        return response.json()

    def get_asset(self, object_id):
        url = f"https://api.atlassian.com/jsm/assets/workspace/{self.workspace_id}/v1/object/{object_id}"
        return self.__get(url)

    def update_issue(self, issue, data):
        self.put(f"api/3/issue/{issue}", data)

    def transition_issue(self, issue, state):
        transition_data = {"transition": {"id": state}}
        self.post(f"api/3/issue/{issue}/transitions", transition_data)

    def close_issue(self, issue):
        self.transition_issue(issue, self.DONE_STATE)
