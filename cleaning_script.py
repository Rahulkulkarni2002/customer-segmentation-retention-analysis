import pandas as pd

# ============================================================
# STEP 1: LOAD
# ============================================================
data = pd.read_csv('online_retail_II.csv', encoding='ISO-8859-1')
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

# ============================================================
# STEP 2: CLEAN
# ============================================================
log = []
log.append(f"Starting rows: {len(data)}")

# 2a. Drop missing Customer ID - can't do customer-level analysis without it
before = len(data)
data = data[data['Customer ID'].notnull()]
log.append(f"Dropped {before - len(data)} rows with missing Customer ID -> {len(data)} remaining")

# 2b. Drop cancelled invoices (Invoice starts with 'C') - not completed purchases
before = len(data)
data = data[~data['Invoice'].astype(str).str.startswith('C')]
log.append(f"Dropped {before - len(data)} cancelled invoice rows -> {len(data)} remaining")

# 2c. Drop administrative/non-product stock codes
before = len(data)
admin_codes = ['M', 'D', 'BANK CHARGES', 'ADJUST', 'AMAZONFEE', 'TEST001', 'CRUK']
data = data[~data['StockCode'].isin(admin_codes)]
log.append(f"Dropped {before - len(data)} administrative/non-product code rows -> {len(data)} remaining")

# 2d. Duplicates - investigated, NOT dropped. Same Invoice number, scattered
# individual line items consistent with real repeated purchases (e.g. same
# product added to cart multiple times), not an export error. Dropping these
# would undercount real purchased quantity and revenue.

# 2e. Remaining zero/negative price rows and internal stock-adjustment rows
# (S/samples, DCGS codes, etc.) - investigated, found 0 remaining after
# upstream filters, already excluded via missing Customer ID.

data['Revenue'] = data['Quantity'] * data['Price']

# ============================================================
# FINAL CHECK
# ============================================================
print("\n".join(log))
print(f"\nFINAL: {len(data)} rows | {data['Customer ID'].nunique()} customers | {data['Invoice'].nunique()} invoices")

data.to_csv('cleaned_retail.csv', index=False)
