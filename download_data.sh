#!/usr/bin/env bash
set -euo pipefail

# 1. Make sure data folder exists
mkdir -p data

# 2. Download the IEEE‑CIS competition files
echo "Downloading IEEE‑CIS fraud dataset…"
kaggle competitions download -c ieee-cis-fraud-detection -p data

# 3. Unzip all CSVs
echo "Extracting CSVs…"
unzip -o data/train_transaction.csv.zip   -d data
unzip -o data/train_identity.csv.zip      -d data
unzip -o data/test_transaction.csv.zip    -d data
unzip -o data/test_identity.csv.zip       -d data
unzip -o data/sample_submission.csv.zip   -d data

# 4. Clean up zip files (optional)
rm data/*.zip

# 5. Merge into single files (using your merge script)
echo "Merging CSVs…"
cd preprocessing
source .venv/bin/activate    # assumes you’ve created this venv already
python merge_csvs.py
deactivate
cd ..

echo "Data download and merge complete. Check data/merged_train.csv and data/merged_test.csv"
