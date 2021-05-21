import boto3
from .auth import client
from .flow import FlowController
from .setflow import SetFlow
from .parse import Parser

# flow_name = 'APIflow_filter'
# profile_name = 'sfde'
# 't-est-bucket'
# flow = FlowController(flow_name, profile_name)
# res = flow.update_flow()
# res = start_flow(flow_name)
# print(res)

if __name__ == "__main__":
    
    # マッピング用設定ファイルの取得
    # S3からSalesforceを前提とする。
    # S3のフォルダプレフィックスとSalesforceオブジェクト名と、
    # フィールドマッピング対応が記載されている。
    p = Parser("data/sample.json")

    conf = p.validate()
    
    # フロー名、フローの説明
    setflow = SetFlow("ApiFlowFromScript", "Api Flow", conf)

    # S3のバケット名、S3のフォルダプレフィックス
    setflow.set_s3("t-est-bucket", "contact")

    # Salesforceのコネクタ名、Salesforceのオブジェクト名
    setflow.set_sf("sfde", "Contact")

    # フローの作成
    setflow.create_flow()
