import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

# Paths
train_txn   = os.path.join(DATA_DIR, "train_transaction.csv")
train_id    = os.path.join(DATA_DIR, "train_identity.csv")
test_txn    = os.path.join(DATA_DIR, "test_transaction.csv")
test_id     = os.path.join(DATA_DIR, "test_identity.csv")

# Load
df_train_txn = pd.read_csv(train_txn)
df_train_id  = pd.read_csv(train_id)
df_test_txn  = pd.read_csv(test_txn)
df_test_id   = pd.read_csv(test_id)

# Merge on TransactionID
df_train = df_train_txn.merge(df_train_id, how="left", on="TransactionID")
df_test  = df_test_txn.merge(df_test_id,  how="left", on="TransactionID")

# Save merged
df_train.to_csv(os.path.join(DATA_DIR, "merged_train.csv"), index=False)
df_test.to_csv(os.path.join(DATA_DIR, "merged_test.csv"),  index=False)

print("Wrote merged_train.csv and merged_test.csv")
