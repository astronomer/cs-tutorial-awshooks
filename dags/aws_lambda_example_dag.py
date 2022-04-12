from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from include.aws_lambda_tools import AWSClient

with DAG('aws_lambda_example_dag',
         start_date=datetime(2019, 1, 1),
         max_active_runs=3,
         schedule_interval=None,
         catchup=False
         ) as dag:

    start = DummyOperator(
        task_id='start'
    )

    python_aws_base = PythonOperator(
        task_id='python_aws_base',
        python_callable=AWSClient().base_invoke_lambda,
        op_kwargs={
          "function_name": "hello-world-python",
          "invocation_type": "RequestResponse",
          "log_type": "Tail",
          "payload": {
              "key1": "hello, world!",
              "key2": "value2",
              "key3": "value3"
          },
          "qualifier": "1"
        }
    )

    python_aws_lambda = PythonOperator(
        task_id='python_aws_lambda',
        python_callable=AWSClient().lambda_invoke_lambda,
        op_kwargs={
            "payload": {
                "key1": "hello, world!",
                "key2": "value2",
                "key3": "value3"
            }
        }
    )

    finish = DummyOperator(
        task_id='finish'
    )

    start >> python_aws_base >> python_aws_lambda >> finish
