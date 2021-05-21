from .auth import client


def start_flow(flow_name):
    response = client.start_flow(
        flowName=flow_name
    )
    return response


class FlowController:
    connector_type = 'Salesforce'
    tasks = []

    def set_map(self, source_field, destination_field):
        self.tasks.append({
            'sourceFields': [
                source_field,
            ],
            'destinationField': destination_field,
            'taskType': 'Map',
            'taskProperties': {
                "DESTINATION_DATA_TYPE": "string",
                "SOURCE_DATA_TYPE": "string"
            }
        })

    def __set_projection(self):
        source_fields = []
        for task in self.tasks:
            if task.get('taskType') != "Map":
                continue
            source_field = task.get('sourceFields')[0]
            source_fields.append(source_field)

        self.tasks.insert(0, {
            "connectorOperator": {
                "Salesforce": "PROJECTION"
            },
            "sourceFields": source_fields,
            "taskProperties": {
                # "DATA_TYPE": "datetime",
                # "LOWER_BOUND": "Lower_Bound_value",
                # "UPPER_BOUND": "Upper_Bound_value"
            },
            "taskType": "Filter"
        })

    def __init__(self, flow_name: str, bucket_name: str, bucket_prefix: str, profile_name: str, sf_object: str) -> None:
        self.destinationFlowConfigList = [{
            'connectorType': self.connector_type,
            'connectorProfileName': profile_name,
            'destinationConnectorProperties': {
                'Salesforce': {
                    'object': sf_object,
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
                    'bucketName': bucket_name,
                    'bucketPrefix': bucket_prefix
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
                "connectorOperator": {
                    "Salesforce": "PROJECTION"
                },
                "sourceFields": [
                    "owner",
                    "Name",
                    "Account:ExternalID1__c",
                ],
                "taskProperties": {
                    # "DATA_TYPE": "datetime",
                    # "LOWER_BOUND": "Lower_Bound_value",
                    # "UPPER_BOUND": "Upper_Bound_value"
                },
                "taskType": "Filter"
            },
            {
                'sourceFields': [
                    'Name',
                ],
                'destinationField': 'LastName',
                'taskType': 'Map',
                'taskProperties': {
                    "DESTINATION_DATA_TYPE": "string",
                    "SOURCE_DATA_TYPE": "string"
                }
            }, {
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
            }, {
                "connectorOperator": {
                    "Salesforce": "VALIDATE_NON_NULL",
                    "S3": "VALIDATE_NON_NULL"
                },
                'sourceFields': [
                    'Account:ExternalID1__c',
                ],
                # 'destinationField': 'AccountId',
                'destinationField': 'Account__ExternalID1__r',
                'taskType': 'Validate',
                # 'taskProperties': {}
                'taskProperties': {
                    "DESTINATION_DATA_TYPE": "reference",
                    "SOURCE_DATA_TYPE": "id"
                }
            }, {
                'sourceFields': [
                    'Account:ExternalID1__c',
                ],
                # 'destinationField': 'AccountId',
                'destinationField': 'Account__ExternalID1__r',
                'taskType': 'Map',
                'taskProperties': {
                    "DESTINATION_DATA_TYPE": "reference",
                    "SOURCE_DATA_TYPE": "id",
                    "DESTINATION_DATA_TYPE": "NULL"
                }
            }
        ]

    def create_flow(self):
        self.__set_projection()
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
