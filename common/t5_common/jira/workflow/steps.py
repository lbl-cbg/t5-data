

def connect():
    path = "./job.yaml"

    # 1. load yaml

    # 2. Create connector

    # 3. Get issue

    return connector, issue

def finish_job():

    parser = argparse.ArgumentParser(description="Set up a database for a Jira workflow tracker")
    args = parser.parse_args()

    connector, issue = connect()

    connector.finish_job(issue)

    connector.close()


def publish_job():

    parser = argparse.ArgumentParser(description="Set up a database for a Jira workflow tracker")
    args = parser.parse_args()

    connector, issue = connect()

    connector.publish_job(issue)

    connector.close()
