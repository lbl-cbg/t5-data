import argparse
import os
import sys
import subprocess
import yaml
import time
from t5_common.jira import JiraConnector
from t5_common.utils import get_logger

from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7523 import PrivateKeyJWT


last_mtime = None
def check_configs(config_path, orig=None):
    """Attempt to load new config.

    Return original config if loading new config failed.
    """
    global last_mtime
    if last_mtime is None:
        last_mtime = os.path.getmtime(config_path)
    curr_mtime = s.path.getmtime(config_path)
    if curr_mtime > last_mtime:
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Updated config from {config_path}")
            last_mtime = curr_mtime
            return config
        except Exception as e:
            logger.error(f"Unable to load config {config_path}", file=sys.stderr)
            return orig


def read_token(path):
    """Helper for reading token or password files"""
    with open(path, 'r') as f:
        return f.read().strip()


def format_query(config):
    return 'project = {project} AND status = "{new_status}"'.format(**config)


def submit_job(issue, config):
    token_url = config.get("token_url", "https://oidc.nersc.gov/c2id/token")
    sfapi_url = config.get("sfapi_url", "https://api.nersc.gov/api/v1.2")
    system = config.get("system", "perlmutter")

    client_id = config['client_id']
    sfapi_key = read_token(config['sfapi_key_file'])

    session = OAuth2Session(
        client_id,
        sfapi_key,
        PrivateKeyJWT(token_url),
        grant_type="client_credentials",
        token_endpoint=token_url
    )
    session.fetch_token()

    try:
        submit_script = "<path to script>" # (e.g., /global/homes/u/username/script.sub)
        r = session.post(f"{sfapi_url}/compute/jobs/{system}",
                          data = {"job": submit_script, "isPath": True})
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script} with issue {issue}: {e}")
    pass


def main():
    parser = argparse.ArgumentParser(description="Poll Jira projects and run a script for each issue.")
    parser.add_argument('config', type=str, help='Path to the YAML configuration file')

    args = parser.parse_args()

    config = None
    while True:
        configs = check_config(args.config, orig=config)

        jc = JiraConnector(jira_host=config['jira_host'],
                           jira_user=config['jira_user'],
                           jira_token=read_token(config['jira_token_file']))

        for project_config in configs['projects']:
            query = format_query(project_config)
            issues = jc.query(query)
            for issue in issues:
                job_id = submit_job(issue, project_config)
                jc.transition_issue(issue, project_config['started_status'])
                jc.add_comment(issue, "Job submitted: Perlmutter job ID {job_id}")

        time.sleep(configs.get('wait_time', 60))

if __name__ == "__main__":
    main()

