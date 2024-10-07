coa_list="""
Cash on Hand 
Checking Account  
Savings Account  
Accounts Receivable  
Inventory   
Prepaid Expenses  
Undeposited Funds  
Furniture and Fixtures 
Office Equipment  
Vehicles   
Accumulated Depreciation  
Security Deposits  
Long-term Investments  
Accounts Payable  
Credit Card Payable 
Sales Tax Payable 
Payroll Liabilities  
Short-term Loans  
Customer Deposits  
Long-term Loans  
Mortgage Payable  
Deferred Revenue  
Common Stock  
Retained Earnings  
Owner's Equity  
Distributions/Withdrawals   
Opening Balance Equity 
Product Sales  
Service Revenue  
Other Revenue  
Sales Discounts  
Sales Returns and Allowances
Interest Income  
Dividend Income  
Gain on Sale of
Miscellaneous Income  
Cost of Goods Sold
Direct Materials  
Direct Labor  
Manufacturing Overhead  
Purchase Discounts  
Purchase Returns and Allowances
Salaries and Wages 
Payroll Taxes  
Employee Benefits  
Rent Expense  
Utilities   
Office Supplies  
Telephone and Internet 
Insurance Expense  
Repairs and Maintenance 
Advertising and Promotion 
Travel and Entertainment 
Professional Fees  
Depreciation Expense  
Amortization Expense  
Interest Expense  
Bank Service Charges 
Bad Debts Expense 
Miscellaneous Expense  
Income Tax Expense 
Deferred Income Tax 
Gain/Loss on Sale of
Unrealized Gain/Loss on Investments
  
"""

# Sample data for COA import
coa_data = [
    ('Assets', 'Current Assets', '1000 - Cash on Hand'),
    ('Assets', 'Current Assets', '1010 - Checking Account'),
    ('Assets', 'Current Assets', '1020 - Savings Account'),
    ('Assets', 'Current Assets', '1030 - Accounts Receivable'),
    ('Assets', 'Current Assets', '1040 - Inventory'),
    ('Assets', 'Current Assets', '1050 - Prepaid Expenses'),
    ('Assets', 'Current Assets', '1060 - Undeposited Funds'),
    ('Assets', 'Fixed Assets', '1500 - Furniture and Fixtures'),
    ('Assets', 'Fixed Assets', '1510 - Office Equipment'),
    ('Assets', 'Fixed Assets', '1520 - Vehicles'),
    ('Assets', 'Fixed Assets', '1530 - Accumulated Depreciation'),
    ('Assets', 'Other Assets', '1700 - Security Deposits'),
    ('Assets', 'Other Assets', '1710 - Long-term Investments'),
    ('Liabilities', 'Current Liabilities', '2000 - Accounts Payable'),
    ('Liabilities', 'Current Liabilities', '2010 - Credit Card Payable'),
    ('Liabilities', 'Current Liabilities', '2020 - Sales Tax Payable'),
    ('Liabilities', 'Current Liabilities', '2030 - Payroll Liabilities'),
    ('Liabilities', 'Current Liabilities', '2040 - Short-term Loans'),
    ('Liabilities', 'Current Liabilities', '2050 - Customer Deposits'),
    ('Liabilities', 'Long-term Liabilities', '2500 - Long-term Loans'),
    ('Liabilities', 'Long-term Liabilities', '2510 - Mortgage Payable'),
    ('Liabilities', 'Long-term Liabilities', '2520 - Deferred Revenue'),
    ('Equity', 'Equity Accounts', '3000 - Common Stock'),
    ('Equity', 'Equity Accounts', '3010 - Retained Earnings'),
    ('Equity', 'Equity Accounts', '3020 - Owner\'s Equity'),
    ('Equity', 'Equity Accounts', '3030 - Distributions/Withdrawals'),
    ('Equity', 'Equity Accounts', '3040 - Opening Balance Equity'),
    ('Revenue', 'Sales Revenue', '4000 - Product Sales'),
    ('Revenue', 'Sales Revenue', '4010 - Service Revenue'),
    ('Revenue', 'Sales Revenue', '4020 - Other Revenue'),
    ('Revenue', 'Sales Revenue', '4030 - Sales Discounts'),
    ('Revenue', 'Sales Revenue', '4040 - Sales Returns and Allowances'),
    ('Revenue', 'Other Income', '4500 - Interest Income'),
    ('Revenue', 'Other Income', '4510 - Dividend Income'),
    ('Revenue', 'Other Income', '4520 - Gain on Sale of Assets'),
    ('Revenue', 'Other Income', '4530 - Miscellaneous Income'),
    ('Cost of Goods Sold', 'COGS', '5000 - Cost of Goods Sold'),
    ('Cost of Goods Sold', 'COGS', '5010 - Direct Materials'),
    ('Cost of Goods Sold', 'COGS', '5020 - Direct Labor'),
    ('Cost of Goods Sold', 'COGS', '5030 - Manufacturing Overhead'),
    ('Cost of Goods Sold', 'COGS', '5040 - Purchase Discounts'),
    ('Cost of Goods Sold', 'COGS', '5050 - Purchase Returns and Allowances'),
    ('Expenses', 'Operating Expenses', '6000 - Salaries and Wages'),
    ('Expenses', 'Operating Expenses', '6010 - Payroll Taxes'),
    ('Expenses', 'Operating Expenses', '6020 - Employee Benefits'),
    ('Expenses', 'Operating Expenses', '6030 - Rent Expense'),
    ('Expenses', 'Operating Expenses', '6040 - Utilities'),
    ('Expenses', 'Operating Expenses', '6050 - Office Supplies'),
    ('Expenses', 'Operating Expenses', '6060 - Telephone and Internet'),
    ('Expenses', 'Operating Expenses', '6070 - Insurance Expense'),
    ('Expenses', 'Operating Expenses', '6080 - Repairs and Maintenance'),
    ('Expenses', 'Operating Expenses', '6090 - Advertising and Promotion'),
    ('Expenses', 'Operating Expenses', '6100 - Travel and Entertainment'),
    ('Expenses', 'Operating Expenses', '6110 - Professional Fees'),
    ('Expenses', 'Operating Expenses', '6120 - Depreciation Expense'),
    ('Expenses', 'Operating Expenses', '6130 - Amortization Expense'),
    ('Expenses', 'Other Expenses', '6500 - Interest Expense'),
    ('Expenses', 'Other Expenses', '6510 - Bank Service Charges'),
    ('Expenses', 'Other Expenses', '6520 - Bad Debts Expense'),
    ('Expenses', 'Other Expenses', '6530 - Miscellaneous Expense'),
    ('Other Accounts', 'Income Tax', '7000 - Income Tax Expense'),
    ('Other Accounts', 'Income Tax', '7010 - Deferred Income Tax'),
    ('Gains & Losses', 'Gains & Losses', '8000 - Gain/Loss on Sale of Assets'),
    ('Gains & Losses', 'Gains & Losses', '8010 - Unrealized Gain/Loss on Investments')
]

