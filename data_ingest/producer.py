import csv
import json
import time
import boto3
import os

# CONFIGURE these via environment variables or hard‑code for now:
STREAM_NAME = os.environ.get("KINESIS_STREAM", "fraud-txn-stream-dev")
CSV_PATH    = os.environ.get("CSV_PATH", "../data/merged_train.csv")
RATE_SEC    = float(os.environ.get("RATE_SEC", "0.05"))  # 20 records/sec

kinesis = boto3.client("kinesis")

def emit_records():
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            payload = {
                "transaction_id": row.get("TransactionID") or None,
                "features": {k: row[k] for k in row if k not in ("isFraud",)},
                "isFraud": int(row["isFraud"])
            }
            kinesis.put_record(
                StreamName=STREAM_NAME,
                Data=json.dumps(payload),
                PartitionKey=str(payload["transaction_id"] or time.time())
            )
            print(f"→ Sent txn {payload['transaction_id']}, fraud={payload['isFraud']}")
            time.sleep(RATE_SEC)

if __name__ == "__main__":
    print(f"Starting producer to stream '{STREAM_NAME}' at {1/RATE_SEC:.1f} rec/sec")
    emit_records()
