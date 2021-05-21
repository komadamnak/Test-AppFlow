import boto3
client = boto3.client('appflow')

destination_flow_config_list = [{
    'connectorType': 'Salesforce',
    'connectorProfileName': 'sfde',
    'destinationConnectorProperties': {
        'Salesforce': {
            'object': 'Contact',
            'errorHandlingConfig': {
                'failOnFirstDestinationError': True,
                'bucketPrefix': 'errors-contact',
                'bucketName': 't-est-bucket'
            },
            'writeOperationType': 'INSERT',
            # Upsertの場合、externalIdとして仕様するフィールドを入力 ※一つまで
            'idFieldNames': []
        }
    }
}]

flow_name = "Test-Flow"
description = 'created from API'
trigger_config = {
    'triggerType': 'OnDemand',
}
source_flow_config = {
    'connectorType': 'S3',
    'sourceConnectorProperties': {
        'S3': {
            'bucketName': 't-est-bucket',
            'bucketPrefix': 'contact'
        },
    }
}

tasks = [
    {
        "connectorOperator": {
            "Salesforce": "PROJECTION"
        },
        "sourceFields": [
            "owner",
            "Name",
        ],
        "taskProperties": {},
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
        'taskProperties': {
            "DESTINATION_DATA_TYPE": "reference",
            "SOURCE_DATA_TYPE": "string"
        }
    }
]

client.create_flow(
    flowName=flow_name,
    description=description,
    triggerConfig=trigger_config,
    sourceFlowConfig=source_flow_config,
    destinationFlowConfigList=destination_flow_config_list,
    tasks=tasks
)
