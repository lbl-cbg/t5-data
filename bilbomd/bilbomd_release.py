import argparse
import os
import sys

from jira import JIRA


parser = argparse.ArgumentParser()
parser.add_argument("bilbomd_dir", help="the output directory from a BilboMD run")
parser.add_argument("jira_issue", help="the Jira issue for this BilboMD run")

args = parser.parse_args()

metadata_json = os.path.join(args.bilbomd_dir, 'metadata.json')
jat_key = None
jat_key_file = os.path.join(args.bilbomd_dir, 'jat_key')
if not os.path.exists(metadata_json):
    # Build payload for posting analysis to JAMO
    outputs = []
    inputs = []
    metadata = {'jira_issue': args.jira_issue}
    for file in os.listdir(args.bilbomd_dir):
        path = os.path.realpath(os.path.join(args.bilbomd_dir, file))
        file_metadata = dict{}
        if file.startswith("ensemble_size"):
            file_metadata['ensemble_size'] = int(file.split("_")[2])
            if file.endswith("pdb"):
                file_metadata['file_format'] = 'pdb'
                file_metadata['compression'] = 'none'
                label = 'protein_model'
            else:
                file_metadata['file_format'] = 'txt'
                file_metadata['compression'] = 'none'
                label = 'ensembles_info'
        elif file == 'const.inp':
            file_metadata['file_format'] = 'txt'
            file_metadata['compression'] = 'none'
        elif file.startswith('README'):
            file_metadata['file_format'] = file.split('.')[:-1]
            file_metadata['compression'] = 'none'
        elif file.startswith('multi_state_model'):
            file_metadata['ensemble_size'] = int(file.split("_")[3])
            file_metadata['file_format'] = 'saxs_dat'
            file_metadata['compression'] = 'none'
        else:
            continue
        outputs.append({'file': path, 'label': label, 'metadata': file_metadata})

    # template data
    td = {'outputs': outputs, 'metadata': metadata, 'inputs': inputs

    host = os.environ['JAMO_HOST']
    curl = Curl(host, appToken=os.environ['BILBOMD_JAMO_TOKEN'])  # BilboMD application token
    resp = curl.post('api/analysis/analysisimport',
                     template_name='bilbomd',
                     template_data=td},
                     location=args.bilbomd_dir)

    if len(resp['warnings']) > 0:
        sys.stdout.write('\n'.join(resp['warnings']) + '\n')
    print(f"Successfully imported results from {args.bilbomd_dir} as {resp['jat_key']}")

    with open(metadata_json, 'w') as f:
        json.dump(td, f, indent=4)

    with open(jat_key_file, "w") as f:
        print(resp['jat_key'], file=f)
else:
    if not os.path.exists(jat_key_file):
        print("Found metadata.json file in {args.bilbo_dir} but no JAT key file (jat_key)", file=sys.stderr)
        exit(1)
    with open(jat_key_file, "r") as f:
        jat_key = f.read().strip()
    print("Data already submitted to JAT")

jamo_url = os.path.join(host, 'analysis', resp['jat_key'])
print(f"You can view analysis at {jamo_url}")

# Connect to Jira
jira_server = os.environ.get('JIRA_HOST', 'https://taskforce5.atlassian.net')
jira_user = os.environ.get('JIRA_USER', 'ajtritt@lbl.gov')
jira_token = os.environ['JIRA_TOKEN']  # You can create a token in Jira account settings

jira = JIRA(server=jira_server, basic_auth=(jira_user, jira_token))

# Update Ussue field designated for connecting to the results
# To figure out the number of the custom field of interest, go to
# Jira -> Settings -> Custom fields (under Fields on the right. Then click on the
# three dots on the right of the field of interest. A small window will pop up. Click
# on Edit Details. This will open another page. The URL of this page ends with
# "id=<NUMBER>". The number here will be the number to append to "customfield_"
# for updating the field through the API.

jira.issue(args.jira_issue).update(fields={'customfield_10112': jamo_url})
print(f"Issue {args.jira_issue} updated successfully.")

jira.transition_issue(issue, '41')
print(f"Issue {jira_issue} marked as Done")
