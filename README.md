当レポジトリでは、AWSのAppFlowをAPIから利用するためのサンプルコードを記載します。
環境は、Python 3.7.6利用し、AWS client libraryとして、boto3を利用します。


## 認証について
上から順に認証情報を検索

1. Passing credentials as parameters in the boto.client() method
2. Passing credentials as parameters when creating a Session object
3. Environment variables
4. Shared credential file (~/.aws/credentials)
5. AWS config file (~/.aws/config)
6. Assume Role provider
7. Boto2 config file (/etc/boto.cfg and ~/.boto)
8. Instance metadata service on an Amazon EC2 instance that has an IAM role configured



### 認証情報の取得
[認証情報の取得](https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/id_credentials_access-keys.html)

### 環境変数を利用した認証方法

```
AWS_SHARED_CREDENTIALS_FILE
```
でコンフィグファイルの位置を指定可能。（デフォルトだと```~/.aws/credentials```）