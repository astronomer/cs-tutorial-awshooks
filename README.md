# Customer Success AWS Lambda Tutorial
This DAG demonstrates how to use the the `AwsBaseHook` and `AwsLambdaHook`

# Prerequisites:
- Astro CLI
- Amazon Web Services Account

# Steps to Use:
### Run the following in your terminal:
1. `git clone git@github.com:astronomer/cs-tutorial-awshooks.git`
2. `cd cs-tutorial-awshooks`
3. `astro d start`

### Add **aws_default** connection to your sandbox
1. Go to your sandbox http://localhost:8080/home
2. Navigate to connections (i.e. Admin >> Connections)
3. Add a new connection with the following parameters
    - Connection Id: aws_default
    - Connection Type: Amazon Web Services
    - Login: *aws_access_key_id*
    - Password: *aws_secret_access_key*
    - Extra: {"region_name": "*your_default_aws_region*"}

Be sure to replace: 
 - *aws_access_key_id*
 - *aws_secret_access_key*
 - *your_default_aws_region* with your actual AWS Default Region (i.e. us-east-1, us-east-2, etc.)

Please note that whichever AWS account parameters that you use here will need proper access to execute AWS Lambda Functions

**FYI**: For more info on the aws_default connection, please click [here](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html)
  
### Create a hello world function in AWS Lambda
In AWS, create a python lambda function called `hello-world-python` that mirrors the following:

```
import json

print('Loading function')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print("value1 = " + event['key1'])
    print("value2 = " + event['key2'])
    print("value3 = " + event['key3'])
    return event['key1']  # Echo back the first key value
    #raise Exception('Something went wrong')
```

___
After following these steps, you should be able to run the tasks in the `aws_lambda_example_dag`. Enjoy!
