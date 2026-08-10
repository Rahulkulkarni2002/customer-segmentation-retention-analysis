import pandas as pd

# ============================================================
# STEP 1: LOAD
# ============================================================
# your original pd.read_csv line here


# ============================================================
# STEP 2: CLEAN
# ============================================================
log = []
log.append(f"Starting rows: {len(data)}")

# 2a. Drop missing Customer ID
before = len(data)
# your filter line
log.append(f"Dropped {before - len(data)} rows with missing Customer ID -> {len(data)} remaining")

# 2b. Drop cancelled invoices
before = len(data)
# your filter line
log.append(f"Dropped {before - len(data)} cancelled invoice rows -> {len(data)} remaining")

# 2c. Drop administrative/non-product stock codes
before = len(data)
admin_codes = ['M', 'D', 'BANK CHARGES', 'ADJUST', 'AMAZONFEE', 'TEST001', 'CRUK']
# your filter line
log.append(f"Dropped {before - len(data)} administrative/non-product code rows -> {len(data)} remaining")

# 2d. Duplicates - investigated, NOT dropped (same Invoice number, scattered
# individual line items consistent with real repeated purchases, not export errors)

# 2e. S (samples) and DCGS codes - investigated, found 0 remaining after
# upstream filters, already excluded via missing Customer ID

# ============================================================
# FINAL CHECK
# ============================================================
print("\n".join(log))
print(f"\nFINAL: {len(data)} rows | {data['Customer ID'].nunique()} customers | {data['Invoice'].nunique()} invoices")

data.to_csv('cleaned_retail.
