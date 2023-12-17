import boto3
import csv
from datetime import datetime

# Initialize the IAM client
iam = boto3.client('iam')

users = iam.list_users()
user_list = []

for key in users['Users']:
    result = {}
   # ManagedPolicies = []
   # InlinePolicies = []
    Groups = []

    result['UserName'] = key['UserName']
    
    ''' attached_policies = iam.list_attached_user_policies(UserName=key['UserName'])
    managed_policies = []

    for policy in attached_policies['AttachedPolicies']:
        managed_policies.append(policy['PolicyName'])

    result['ManagedPolicies'] = managed_policies

    # List inline policies for the user
    inline_policies = iam.list_user_policies(UserName=key['UserName'])
    inline_policy_names = inline_policies.get('PolicyNames', [])

    inline_policies = iam.list_user_policies(UserName=key['UserName'])
    result['InlinePolicies'] = inline_policies.get('PolicyNames', [])


    #result['InlinePolicies'] = InlinePolicies
    '''
    # List IAM groups for the user
    List_of_Groups = iam.list_groups_for_user(UserName=key['UserName'])

    for Group in List_of_Groups['Groups']:
        Groups.append(Group['GroupName'])
    
    result['Groups'] = Groups if Groups else 'null'

    user_tags = iam.list_user_tags(UserName=key['UserName'])
    tags = user_tags.get('Tags', [])

    result['Tags'] = tags if tags else 'null'
    
    user_list.append(result)

# Create a CSV filename with a timestamp
csv_filename = f'user_info_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'

# Write the user data to a CSV file
with open(csv_filename, mode='w', newline='') as csv_file:
    fieldnames = ['UserName','Groups', 'Tags']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in user_list:
        writer.writerow(row)

# Print a message indicating that the CSV file has been generated
print(f"CSV file '{csv_filename}' generated for IAM users.")
