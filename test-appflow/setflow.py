from .parse import Config, Parser
from .auth import client


def create_map_task(source, destination):
    return {
        'sourceFields': [source],
        'destinationField': destination,
        'taskType': 'Map',
        'taskProperties': {}
    }


def create_projection_filter_task(*sources):
    return{
        "connectorOperator": {
            "S3": "PROJECTION",
            "Salesforce": "PROJECTION"
        },
        "sourceFields": list(sources),
        "taskProperties": {},
        "taskType": "Filter"
    }


def create_destination_flow_config_list(connector_type, profile_name, sf_object):
    return [{
        'connectorType': connector_type,
        'connectorProfileName': profile_name,
        'destinationConnectorProperties': {
            'Salesforce': {
                'object': sf_object,
                # 'errorHandlingConfig': {
                #     'failOnFirstDestinationError': True,
                #     'bucketPrefix': 'errors-contact',
                #     'bucketName': 't-est-bucket'
                # },
                'writeOperationType': 'INSERT'  # | 'UPSERT' | 'UPDATE'
            }
        }
    }]


def create_source_flow_config(bucket_name, bucket_prefix):
    return {
        'connectorType': 'S3',
        'sourceConnectorProperties': {
            'S3': {
                'bucketName': bucket_name,
                'bucketPrefix': bucket_prefix
            }
        }
    }


class SetFlow:
    config: Config
    connector_type = 'Salesforce'
    destinationFlowConfigList = None
    sourceFlowConfig = None
    triggerConfig = {
        'triggerType': 'OnDemand',
    }
    tasks = []

    def __init__(self, flow_name: str, description: str, config: Config) -> None:
        self.config = config
        for o in config.mappings_obj:
            print("config", o.destination, o.source)
        self.flow_name = flow_name
        self.description = description

    def set_sf(self, profile_name, sf_object):
        self.destinationFlowConfigList = create_destination_flow_config_list(
            'Salesforce', profile_name, sf_object)

    def set_s3(self, bucket_name, bucket_prefix):
        self.sourceFlowConfig = create_source_flow_config(
            bucket_name, bucket_prefix)

    def __set_tasks(self):
        sources = []
        for obj in self.config.mappings_obj:
            sources.append(obj.source)
            map_task = create_map_task(obj.source, obj.destination)
            self.tasks.append(map_task)
        self.tasks.insert(0, create_projection_filter_task(*sources))

    def create_flow(self):
        self.__set_tasks()
        print(self.tasks)
        print(self.destinationFlowConfigList)
        response = client.create_flow(
            flowName=self.flow_name,
            description=self.description,
            triggerConfig=self.triggerConfig,
            sourceFlowConfig=self.sourceFlowConfig,
            destinationFlowConfigList=self.destinationFlowConfigList,
            tasks=self.tasks
        )
        return response

    def update_flow(self):
        response = client.update_flow(
            flowName=self.flow_name,
            description=self.description,
            triggerConfig=self.triggerConfig,
            sourceFlowConfig=self.sourceFlowConfig,
            destinationFlowConfigList=self.destinationFlowConfigList,
            tasks=self.tasks
        )
        return response
