from .auth import client


def start_flow(flow_name):
    response = client.start_flow(
        flowName=flow_name
    )
    return response


class Flow:
    def __init__(self, flow_name: str) -> None:
        self.destinationFlowConfigList = [{
            'connectorType': 'Salesforce',
            'connectorProfileName': 'sfde',
            'destinationConnectorProperties': {
                'Salesforce': {
                    'object': 'Contact',
                    # 'idFieldNames': [
                    #     'Id'
                    #     'AccountId',
                    #     'Account:ExternalID1__c'
                    # ],
                    'errorHandlingConfig': {
                        'failOnFirstDestinationError': True,
                        'bucketPrefix': 'errors-contact',
                        'bucketName': 't-est-bucket'
                    },
                    'writeOperationType': 'INSERT'  # | 'UPSERT' | 'UPDATE'
                }
            }
        }]
        self.flowName = flow_name
        self.description = 'created from API'
        self.triggerConfig = {
            'triggerType': 'OnDemand',
        }
        self.sourceFlowConfig = {
            'connectorType': 'S3',
            'sourceConnectorProperties': {
                'S3': {
                    'bucketName': 't-est-bucket',
                    'bucketPrefix': 'contact'
                },
            }
        }

        self.tasks = [
            # {
            #     'sourceFields': [
            #         'Account:ExternalID1__c',
            #     ],
            #     'destinationField': 'AccountId',
            #     'taskType': 'Map',
            #     # 'taskType': 'Arithmetic' | 'Filter' | 'Map' | 'Mask' | 'Merge' | 'Truncate' | 'Validate',
            #     'taskProperties': {
            #         "DESTINATION_DATA_TYPE": "reference",
            #         "SOURCE_DATA_TYPE": "id"
            #     }
            # },
            {
                'connectorOperator': {
                    'S3': 'PROJECTION'
                },
                'sourceFields': [
                    '名前',
                ],
                'destinationField': 'LastName',
                'taskType': 'Map',
                'taskProperties': {
                    "DESTINATION_DATA_TYPE": "string",
                    "SOURCE_DATA_TYPE": "string"
                }
            }, {
                'connectorOperator': {
                    'S3': 'PROJECTION'
                },
                'sourceFields': [
                    'owner',
                ],
                'destinationField': 'OwnerId',
                'taskType': 'Map',
                # 'taskProperties': {}
                'taskProperties': {
                    "DESTINATION_DATA_TYPE": "reference",
                    "SOURCE_DATA_TYPE": "string"
                }
            }
        ]

    def create_flow(self):
        response = client.create_flow(
            flowName=self.flowName,
            description=self.description,
            triggerConfig=self.triggerConfig,
            sourceFlowConfig=self.sourceFlowConfig,
            destinationFlowConfigList=self.destinationFlowConfigList,
            tasks=self.tasks
        )
        return response

    def update_flow(self):
        response = client.update_flow(
            flowName=self.flowName,
            description=self.description,
            triggerConfig=self.triggerConfig,
            sourceFlowConfig=self.sourceFlowConfig,
            destinationFlowConfigList=self.destinationFlowConfigList,
            tasks=self.tasks
        )
        return response

# response = client.create_flow(
#     flowName='string',
#     description='created from API',
#     triggerConfig={
#         'triggerType': 'OnDemand',
#     },
#     sourceFlowConfig={
#         'connectorType': 'S3',
#         'connectorProfileName': 'string',
#         'sourceConnectorProperties': {
#             'S3': {
#                 'bucketName': 'string',
#                 'bucketPrefix': 'string'
#             },
#         }
#     },
#     destinationFlowConfigList={
#         'connectorType': 'Salesforce',
#         'connectorProfileName': 'sfdc',
#         'destinationConnectorProperties': {
#             'Salesforce': {
#                 'object': 'string',
#                 'idFieldNames': [
#                     'string',
#                 ],
#                 'errorHandlingConfig': {
#                     'failOnFirstDestinationError': True | False,
#                     'bucketPrefix': 'string',
#                     'bucketName': 'string'
#                 },
#                 'writeOperationType': 'INSERT' | 'UPSERT' | 'UPDATE'
#             }
#         }
#     }
# )
