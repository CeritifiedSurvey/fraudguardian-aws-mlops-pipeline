import os
import json
import boto3
import pandas as pd
from io import BytesIO

# Initialize the S3 client
s3 = boto3.client("s3")

# You can also set these as Lambda environment variables
RAW_BUCKET       = os.environ.get("RAW_BUCKET", "raw-fraud-data-bucket-dev")
PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "processed-fraud-data-bucket-dev")

def handler(event, context):
    """
    Lambda handler to transform raw JSON events in S3
    into Parquet and write to the processed bucket.
    """
    for record in event["Records"]:
        src_bucket = record["s3"]["bucket"]["name"]
        src_key    = record["s3"]["object"]["key"]

        # 1) Download the raw JSON file
        obj = s3.get_object(Bucket=src_bucket, Key=src_key)
        raw_bytes = obj["Body"].read()
        raw_text  = raw_bytes.decode("utf-8")

        # 2) Parse one JSON object per line
        rows = [json.loads(line) for line in raw_text.splitlines()]
        df   = pd.json_normalize(rows)

        # 3) Serialize to Parquet in‑memory
        out_buffer = BytesIO()
        df.to_parquet(out_buffer, index=False)

        # 4) Construct destination key
        dest_key = src_key.replace("raw-data/", "processed-data/") \
                          .rsplit(".", 1)[0] + ".parquet"

        # 5) Upload to processed bucket
        s3.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=dest_key,
            Body=out_buffer.getvalue()
        )
