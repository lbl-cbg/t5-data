import argparse
import os
import re
import sys
import subprocess
import yaml
import time

from .jira import JiraConnector
from ..utils import get_logger, read_token


logger = get_logger()


def check_config(config_path):
    """Attempt to load new config.

    Return original config if loading new config failed.
    """
    try:
        with open(config_path, 'r') as file:
            ret = yaml.safe_load(file)
        logger.info(f"Updated config from {config_path}")
        last_mtime = curr_mtime
    except Exception as e:
        logger.error(f"Unable to load config {config_path}: {e}", file=sys.stderr)


def format_query(config):
    return 'project = {project} AND status = "{new_status}"'.format(**config)


def process_issue(issue, project_config, config):
    env = os.environ.copy()
    env['JIRA_HOST'] = config['host']
    env['JIRA_USER'] = config['user']
    env['JIRA_TOKEN'] = read_token(config['token_file'])

    command = re.split(r'\s+', project_config['command'])
    command.append(issue)

    try:
        logger.info(f"Processing {issue}: {' '.join(command)}")
        result = subprocess.run(command, env=env, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Unable to run command {' '.join(command)}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Poll Jira projects and run a script for each issue.")
    parser.add_argument('config', type=str, help='Path to the YAML configuration file')
    args = parser.parse_args()

    config = None

    config = check_config(args.config, orig=config)

    jc = JiraConnector(jira_host=config['host'],
                       jira_user=config['user'],
                       jira_token=read_token(config['token_file']))

    for project_config in config['projects']:
        query = format_query(project_config)
        issues = jc.query(query)['issues']
        for issue in issues:
            job_id = process_issue(issue['key'], project_config, config)


if __name__ == "__main__":
    main()
