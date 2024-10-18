import argparse
import sys

from jira import JIRA


parser = argparse.ArgumentParser()
parser.add_argument("bilbomd_dir", help="the output directory from a BilboMD run")
parser.add_argument("jira_issue", help="the Jira issue for this BilboMD run")

args = parser.parse_args()

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
curl = Curl(host, appToken="JPLZ0KV3AHIEJOJXL2Q3QAXCB5ZSTRJ9")  # BilboMD application token
resp = curl.post('api/analysis/analysisimport',
                 template_name='bilbomd',
                 template_data=td},
                 location=args.bilbomd_dir)

if len(resp['warnings']) > 0:
    sys.stdout.write('\n'.join(resp['warnings']) + '\n')
print(f"Successfully imported results from {args.bilbomd_dir} as {resp['jat_key']}")
jamo_url = os.path.join(host, 'analysis', resp['jat_key'])
print(f"You can view analysis at {jamo_url}")

with open(os.path.join(args.bilbomd_dir, 'metadata.json'), 'w') as f:
    json.dump(td, f, indent=4)

# Connect to Jira
jira_server = os.environ.get('JIRA_HOST', 'https://taskforce5.atlassian.net')
jira_user = 'sclassen@lbl.gov'
jira_token = os.environ['JIRA_TOKEN']  # You can create a token in Jira account settings

jira = JIRA(server=jira_server, basic_auth=(jira_user, jira_token))

# Update Ussue field designated for connecting to the results
jira.issue(args.jira_issue).update(fields: {'Jamo Results': jamo_url})

print(f"Issue {args.jira_issue} updated successfully.")
