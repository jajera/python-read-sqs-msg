# python-read-sqs-msg

```bash
export AWS_VAULT_FILE_PASSPHRASE="$(cat /root/.awsvaultk)"
```

```bash
aws-vault exec dev -- terraform -chdir=./terraform/01 init
```

```bash
aws-vault exec dev -- terraform -chdir=./terraform/01 apply --auto-approve
```

```bash
source ./terraform/01/terraform.tmp
```

```bash
export QUEUE_URL=<https://sqs>.<REGION>.amazonaws.com/<ACCOUNT_ID>/<SQS_NAME>
export QUEUE_URL=https://sqs.ap-southeast-1.amazonaws.com/615890063537/sqs-fds8w9mk
```

```bash
python ./send_heartbeat/lambda_function.py
```

```bash
python ./process_sqs_msg/lambda_function.py
```

```bash
mkdir -p ./terraform/02/external
```

```bash
zip -r -j ./terraform/02/external/process_sqs_msg.zip ./process_sqs_msg
```

```bash
aws-vault exec dev -- terraform -chdir=./terraform/02 init
```

```bash
aws-vault exec dev -- terraform -chdir=./terraform/02 apply --auto-approve
```
