import argparse
import asyncio
import os
from os.path import abspath, relpath
import re
import sys
import subprocess
import yaml
import time

from . import JiraConnector
from .utils import load_config, WF_FILENAME

from ..utils import get_logger, read_token


logger = get_logger()


def format_query(config):
    return 'project = {project} AND status = "{new_status}"'.format(**config)


async def process_issue(issue, project_config, config):
    # Set up environment to run subprocess in
    env = os.environ.copy()
    env['JIRA_HOST'] = config['host']
    env['JIRA_USER'] = config['user']
    env['JIRA_TOKEN'] = read_token(config['token_file'])

    # Set up the command to run in the subprocess
    command = re.split(r'\s+', project_config['command'])
    command.append(issue)

    # Set up the working directory to run the job in
    wd = os.path.join(config['working_directory'], issue['key'])
    if os.path.exists(wd):
        raise RuntimeError(f"workflow already started for {issue['key']} - {wd} already exists")
    else:
        os.mkdir(wd)

    # Add workflow info to the working directory for subsequence steps
    wf_info = {
            'issue': issue['key'],
            'wfm_database': relpath(abspath(config['database']), abspath(wd)),
            }
    with open(os.path.join(wd, WF_FILENAME), 'r') as f:
        json.dump(wf_info, f)

    # Call the job command in a subprocess
    logger.info(f"Processing {issue['key']}: {' '.join(command)}")
    process = await asyncio.create_subprocess_exec(
        command, *command[1:],
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        env=env,
        cwd=wd,
    )
    # Read the output and error streams
    stdout, _ = await process.communicate()

    if process.returncode != 0:
        logger.error(f"Processing {issue['key']} failed:\n{stdout.decode()}")
    else:
        logger.error(f"Processing {issue['key']} succeeded:\n{stdout.decode()}")

    return process.returncode


def check_jira(config):
    # Connect to Jira
    jc = JiraConnector(jira_host=config['host'],
                       jira_user=config['user'],
                       jira_token=read_token(config['token_file']))

    # Check each project queue, and create a new job for each new issue
    tasks = list()
    for project_config in config['projects']:
        query = format_query(project_config)
        issues = jc.query(query)['issues']
        for issue in issues:
            tasks.append(process_issue(issue['key'], project_config, config))
    results = asyncio.gather(tasks)


def main():
    parser = argparse.ArgumentParser(description="Poll Jira projects and run a script for each issue.")
    parser.add_argument('config', type=str, help='Path to the YAML configuration file')
    args = parser.parse_args()

    config = None

    config = load_config(args.config)
    check_jira(config)


if __name__ == "__main__":
    main()
