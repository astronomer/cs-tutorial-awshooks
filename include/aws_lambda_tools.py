import json
import botocore.response as br
from airflow.providers.amazon.aws.hooks.lambda_function import AwsLambdaHook
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook

class AWSClient:
    def __init__(self):
        self.aws_base_hook = AwsBaseHook(client_type="lambda")
        self.aws_lambda_hook = AwsLambdaHook(function_name="hello-world-python")

    def labmda_invoke_lambda(self, payload):
        json_payload = json.dumps(payload, indent=2).encode('utf-8')
        response = self.aws_lambda_hook.invoke_lambda(payload=json_payload)
        decoded_response = json.loads(response['Payload'].read().decode("utf-8"))
        return decoded_response

    def base_invoke_lambda(self, function_name, invocation_type, log_type, payload, qualifier):
        response = self.aws_base_hook.conn.invoke( #this is the equivalent for boto3 for lambda
            FunctionName=function_name,
            InvocationType=invocation_type,
            LogType=log_type,
            Payload=json.dumps(payload, indent=2).encode('utf-8'),
            Qualifier=qualifier
        )
        decoded_response = json.loads(response['Payload'].read().decode("utf-8"))
        return decoded_response