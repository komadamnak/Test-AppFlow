
import os
import boto3

client = boto3.client('appflow')

os.environ.setdefault('AWS_SHARED_CREDENTIALS_FILE',
                      os.path.join(__file__, '..', '.config'))


class Authenticator:
    pass
