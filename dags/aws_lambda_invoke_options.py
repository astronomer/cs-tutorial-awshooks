import json
from datetime import datetime, timedelta

import boto3
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.lambda_function import LambdaHook
from airflow.providers.amazon.aws.operators.aws_lambda import (
    AwsLambdaInvokeFunctionOperator,
)

lambda_payload = json.dumps(
    {"SampleEvent": {"SampleData": {"Name": "XYZ", "DoB": "1975-01-01"}}}
)

# Use boto3 to connect with lambda
def lambda_boto3():
    lambda_region = "us-east-1"
    lambda_name = "my_lambda_function"
    lambda_client = boto3.client(
        "lambda",
        region_name=lambda_region,
        # store aws credentials as variables
        aws_access_key_id=Variable.get("secret_aws_access_key_id"),
        aws_secret_access_key=Variable.get("secret_aws_secret_access_key"),
    )
    response = lambda_client.invoke(
        FunctionName=lambda_name, InvocationType="Event", Payload=lambda_payload
    )
    print("Response--->", response)


# Use LambdaHook to connect with lambda
def lamba_hook_func():
    hook = LambdaHook(aws_conn_id="aws_default")
    response = hook.invoke_lambda(
        function_name="my_lambda_function",
        log_type="None",
        qualifier="$LATEST",
        invocation_type="RequestResponse",
        payload=lambda_payload,
    )
    print("Response--->", response)


with DAG(
    dag_id="lambda-invoke-options",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    schedule_interval=None,
) as dag:
    # Use boto3 to connect with lambda
    lambda_boto3 = PythonOperator(
        task_id="lambda_boto3",
        python_callable=lambda_boto3,
    )

    # Use LambdaHook to connect with lambda
    lambda_hook = PythonOperator(
        task_id="lambda_hook",
        python_callable=lamba_hook_func,
    )

    # Use AwsLambdaInvokeFunctionOperator to connect with lambda
    lambda_invoke_operator = AwsLambdaInvokeFunctionOperator(
        task_id="lambda_invoke_operator",
        function_name="my_lambda_function",
        payload=lambda_payload,
        aws_conn_id="aws_default",
    )

    lambda_boto3 >> lambda_hook >> invoke_lambda_function
