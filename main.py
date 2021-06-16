import requests
import os
from dotenv import load_dotenv
from dateutil import parser


from constants import url, url_base

load_dotenv()


API_KEY = os.getenv("API_KEY")
HEADERS = {'content-type': 'application/json', 'X-Api-Key': API_KEY}
NAME = os.getenv('NAME')


def get_workspace_and_user_id():
    """
    Get workspace and user id of client
    :return: workspace id and user id
    """
    response = requests.get(url_base, headers=HEADERS)
    workspace_id = response.json()['activeWorkspace']
    user_id = response.json()['id']
    return workspace_id, user_id


def get_project_id(workspace_id):
    """
    Get project id
    :param workspace_id: workspace id
    :return: project id
    """
    project_id = None
    api_projects = f'/workspaces/{workspace_id}/projects'
    api_url = url + api_projects
    response = requests.get(api_url, headers=HEADERS)
    response_projects = response.json()
    for project in response_projects:
        if project['name'] == NAME:
            project_id = project['id']
    return project_id


def get_all_tasks(workspace_id, project_id):
    """
    Get all tasks name and their ids
    :param workspace_id: workspace id
    :param project_id: project id
    :return: list of dicts with names and ids
    """
    tasks = list()
    tasks_url = f'/workspaces/{workspace_id}/projects/{project_id}/tasks'
    api_url = url + tasks_url
    response = requests.get(api_url, headers=HEADERS)
    response_tasks = response.json()
    for task in response_tasks:
        tasks.append({'name': task['name'], 'id': task['id']})
    return tasks[::-1]


def get_data_report(workspace_id, user_id, tasks):
    """
    Get data needed for report
    :param workspace_id: workspace id
    :param user_id: user id
    :param tasks: ist of dicts with names and ids
    :return: list of dicts with needed info like name, id, start_date, end_date and diff
    """
    time_entry_url = f'/workspaces/{workspace_id}/user/{user_id}/time-entries'
    api_url = url + time_entry_url
    response = requests.get(api_url, headers=HEADERS)
    i = 0
    report = list()
    for task in response.json()[::-1][:-1]:
        date_start = task['timeInterval']['start']
        date_end = task['timeInterval']['end']
        date_start = parser.isoparse(date_start)
        date_end = parser.isoparse(date_end)
        diff = date_end - date_start
        report.append({'task_name': tasks[i]['name'],
                       'task_id': task['taskId'],
                       'date_start': date_start,
                       'date_end': date_end,
                       'diff': diff})
        i += 1
    return report


def report_by_tasks(data):
    """
    Print Report sorted by tasks
    :param data: list of dicts
    :return: None
    """
    for row in data:
        print(row["task_name"])
        print(row['task_id'])
        print(row['date_start'])
        print(row['date_end'])
        print(row['diff'])


def report_by_time(data):
    """
    Print Report sorted by diff
    :param data: list of dicts
    :return: None
    """
    data = sorted(data, key=lambda x: x['diff'], reverse=True)
    for row in data:
        print(row["task_name"])
        print(row['task_id'])
        print(row['date_start'])
        print(row['date_end'])
        print(row['diff'])


if __name__ == "__main__":
    workspace_id, user_id = get_workspace_and_user_id()
    project_id = get_project_id(workspace_id)
    names = get_all_tasks(workspace_id, project_id)
    "NAMES AND IDS OF TASKS"
    print(names)
    report = get_data_report(workspace_id, user_id, names)
    print("BY TASKS")
    report_by_tasks(report)
    print("BY TIME")
    report_by_time(report)
