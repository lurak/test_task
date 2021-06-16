import requests
import os
from dotenv import load_dotenv

load_dotenv()
from constants import url, url_base

API_KEY = os.getenv("API_KEY")
HEADERS = {'content-type': 'application/json', 'X-Api-Key': API_KEY}
NAME = os.getenv('NAME')


def get_workspace_id():
    response = requests.get(url_base, headers=HEADERS)
    workspace_id = response.json()['activeWorkspace']
    return workspace_id


def get_project_id(workspace_id):
    project_id = None
    api_projects = f'/workspaces/{workspace_id}/projects'
    api_url = url + api_projects
    response = requests.get(api_url, headers=HEADERS)
    json_response_projects = response.json()
    for project in json_response_projects:
        if project['name'] == NAME:
            project_id = project['id']
    return project_id


def get_all_tasks(workspace_id, project_id):
    tasks = list()
    a = f'/workspaces/{workspace_id}/projects/{project_id}/tasks'
    api_url = url + a
    response = requests.get(api_url, headers=HEADERS)
    json_response_projects = response.json()
    for task in json_response_projects:
        tasks.append(task['name'])
    return tasks


if __name__ == "__main__":
    workspaceId = get_workspace_id()
    projectId = get_project_id(workspaceId)
    names = get_all_tasks(workspaceId, projectId)
    print(names)
