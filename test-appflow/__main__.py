
import os
import boto3

client = boto3.client('appflow')


class Authenticator:
    pass


# response = client.create_connector_profile(
#     connectorProfileName='appflow-sfdc-test',
#     connectorType='Salesforce',
#     connectionMode='Public',
#     connectorProfileConfig={
#         'connectorProfileProperties': {
#             'Salesforce': {
#                 'instanceUrl': 'https://sohobbinc6-dev-ed.lightning.force.com',
#                 'isSandboxEnvironment': True
#             },
#             # consumer 3MVG95mg0lk4batgXlBquJ4u4AMiZGr0j.C42emQFYbovd1SFOcFsKyTYowRvvQp15n9AdjW1ZEKMNgLz2sY.
#             # consumerp 3C55241BE04D672F576FE730CD03B933BCC528D77A61A7B8A8A1107AF0B1B9E3
#         },  # c5QVe7qOmHffliTtZd1pLhHsW,
#         'connectorProfileCredentials': {
#             'Salesforce': {
#                 'oAuthRequest': {
#                     'authCode': '3MVG95mg0lk4batgXlBquJ4u4AMiZGr0j.C42emQFYbovd1SFOcFsKyTYowRvvQp15n9AdjW1ZEKMNgLz2sY.',
#                     'redirectUri': 'https://sohobbinc6-dev-ed.appflow.lightning.force.com'
#                 },
#                 "clientCredentialsArn": "arn:aws:secretsmanager:3MVG95mg0lk4batgXlBquJ4u4AMiZGr0j.C42emQFYbovd1SFOcFsKyTYowRvvQp15n9AdjW1ZEKMNgLz2sY.:948533486867:3C55241BE04D672F576FE730CD03B933BCC528D77A61A7B8A8A1107AF0B1B9E3"
#                 # arn:aws:secretsmanager:$region:$account:secret:$secret
#             }
#         }
#     }
# )

from .flow import Flow, start_flow
flow_name = 'APIFlow1'
flow = Flow(flow_name)
# res = flow.create_flow()
res = flow.update_flow()
# res = start_flow(flow_name)
print(res)
