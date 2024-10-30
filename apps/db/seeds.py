default_coa = [
    # (biz_type, account_type, account_subtype, parent_account, sub_account, coa_note)
    (11, 'Assets', 'Cash and Bank', '1000 Cash and Cash Equivalents', '1000 Cash and cash equivalents account', 'note'),
    (11, 'Assets', 'Cash and Bank', '1000 Cash and Cash Equivalents', '1010 Petty Cash', 'Petty cash account'),
    (11, 'Assets', 'Cash and Bank', '1000 Cash and Cash Equivalents', '1020 Bank Accounts',
     'Bank accounts for the business'),
    (11, 'Assets', 'Cash and Bank', '1000 Cash and Cash Equivalents', '1030 Short-Term Investments',
     'Short-term investments'),

    (11, 'Assets', 'Current Assets', '1100 Accounts Receivable', '1100 Accounts Receivable',
     'Accounts receivable account'),
    (11, 'Assets', 'Current Assets', '1100 Accounts Receivable', '1110 Trade Receivables',
     'Sales from crops, livestock, forest products, etc.'),
    (11, 'Assets', 'Current Assets', '1100 Accounts Receivable', '1120 Retainage Receivable',
     'Retainage receivable (if applicable)'),
    (11, 'Assets', 'Current Assets', '1100 Accounts Receivable', '1130 Allowance for Doubtful Accounts',
     'Retainage receivable (if applicable)'),

    (11, 'Assets', 'Current Assets', '1200 Inventory', '1200 Inventory', 'Inventory account'),
    (11, 'Assets', 'Current Assets', '1200 Inventory', '1210 Livestock Inventory', 'Livestock inventory'),
    (11, 'Assets', 'Current Assets', '1200 Inventory', '1220 Crop Inventory', 'Crop inventory'),
    (11, 'Assets', 'Current Assets', '1200 Inventory', '1230 Timber Inventory', 'Forestry-related businesses'),
    (11, 'Assets', 'Current Assets', '1200 Inventory', '1240 Fish Inventory', 'Fishing operations'),
    (11, 'Assets', 'Current Assets', '1200 Inventory', '1250 Raw Materials', 'Seeds, feed, etc.'),
    (11, 'Assets', 'Current Assets', '1200 Inventory', '1260 Supplies Inventory',
     'Farming, forestry, or fishing supplies'),

    (11, 'Assets', 'Current Assets', '1300 Prepaid Expenses', '1300 Prepaid Expenses', 'Prepaid expenses account'),
    (11, 'Assets', 'Current Assets', '1300 Prepaid Expenses', '1310 Prepaid Insurance', 'Insurance'),
    (11, 'Assets', 'Current Assets', '1300 Prepaid Expenses', '1320 Prepaid Feed and Seed', 'note'),
    (11, 'Assets', 'Current Assets', '1300 Prepaid Expenses', '1330 Prepaid Licenses and Permits',
     'hunting, fishing, or forestry licenses'),

    (11, 'Assets', 'PPE', '1400 Long-Term Assets', '1400 Long-Term Assets', 'Long-term assets account'),
    (11, 'Assets', 'PPE', '1400 Long-Term Assets', '1410 Land', 'note'),
    (11, 'Assets', 'PPE', '1400 Long-Term Assets', '1411 Improvements to Land (Drainage, fencing, irrigation systems)',
     'note'),
    (11, 'Assets', 'PPE', '1400 Long-Term Assets', '1420 Buildings ', 'note'),
    (11, 'Assets', 'PPE', '1400 Long-Term Assets', '1421 Accumulated Depreciation - Buildings', 'note'),
    (11, 'Assets', 'PPE', '1400 Long-Term Assets',
     '1430 Machinery and Equipment (Tractors, combines, logging machinery, etc.)', 'note'),
    (11, 'Assets', 'PPE', '1400 Long-Term Assets', '1431 Accumulated Depreciation - Machinery ', 'note'),
    (11, 'Assets', 'PPE', '1400 Long-Term Assets', '1440 Vehicles (Trucks, ATVs, fishing boats, etc.) ', 'note'),
    (11, 'Assets', 'PPE', '1400 Long-Term Assets', '1441 Accumulated Depreciation - Vehicles ', 'note'),
    (11, 'Assets', 'PPE', '1400 Long-Term Assets', '1450 Timberlands (For forestry businesses)', 'note'),
    (11, 'Assets', 'PPE', '1400 Long-Term Assets', '1460 Fisheries Equipment (Boats, nets, etc.) ', 'note'),

    (11, 'Assets', 'Other Assets', '1500 Other Assets', '1500 Other Assets', 'note'),
    (11, 'Assets', 'Other Assets', '1500 Other Assets', '1510 Deposits', 'note'),

    # Liabilities
    (11, 'Liabilities', 'Current Liabilities', '2000 Accounts Payable', 'Accounts payable account', 'note'),
    (11, 'Liabilities', 'Current Liabilities', '2000 Accounts Payable', '2010 Trade Payables',
     'Trade payables from suppliers'),
    (11, 'Liabilities', 'Current Liabilities', '2000 Accounts Payable', '2020 Retainage Payable (if applicable)',
     'note'),

    (11, 'Liabilities', 'Current Liabilities', '2100 Payroll Liabilities', '2100 Payroll Liabilities', 'note'),
    (11, 'Liabilities', 'Current Liabilities', '2100 Payroll Liabilities', '2110 Salaries Payable', 'note'),
    (11, 'Liabilities', 'Current Liabilities', '2100 Payroll Liabilities', '2120 Employee Benefits Payable', 'note'),
    (11, 'Liabilities', 'Current Liabilities', '2100 Payroll Liabilities',
     '2130 CPP and EI Payable (Canada Pension Plan and Employment Insurance)', 'note'),
    (11, 'Liabilities', 'Current Liabilities', '2100 Payroll Liabilities',
     '2140 Worker Compensation Payable (for farm or forestry workers)', 'note'),

    (11, 'Liabilities', 'Current Liabilities', '2200 Short-Term Loans', '2200 Short-Term Loans',
     'Short-term loans account'),
    (11, 'Liabilities', 'Current Liabilities', '2200 Short-Term Loans', '2210 Bank Overdraft',
     'Short-term loans account'),
    (11, 'Liabilities', 'Current Liabilities', '2200 Short-Term Loans',
     '2220 Agricultural Loan Payable (Short-term operating loans)', 'Short-term loans account'),

    (11, 'Liabilities', 'Accrued Liabilities', '2300 Accrued Liabilities', '', ''),

    (11, 'Liabilities', 'Accrued Liabilities', '2300 Accrued Liabilities', '2310 Accrued Interest (On loans)', ''),
    (11, 'Liabilities', 'Accrued Liabilities', '2300 Accrued Liabilities', '2320 Accrued Payroll', ''),
    (11, 'Liabilities', 'Accrued Liabilities', '2300 Accrued Liabilities',
     '2330 Accrued Expenses (e.g., utilities, repairs)', ''),

    (11, 'Liabilities', 'Taxes Payable', '2400 Taxes Payable', '', ''),
    (11, 'Liabilities', 'Taxes Payable', '2400 Taxes Payable', '2410 GST/HST Payable', ''),
    (11, 'Liabilities', 'Taxes Payable', '2400 Taxes Payable', '2420 PST Payable (if applicable by province)', ''),
    (
    11, 'Liabilities', 'Taxes Payable', '2400 Taxes Payable', '2430 Income Taxes Payable (Federal and provincial)', ''),

    (11, 'Liabilities', 'Long-Term Liabilities', '2500 Long-Term Liabilities', '', ''),
    (11, 'Liabilities', 'Long-Term Liabilities', '2500 Long-Term Liabilities',
     '2510 Mortgage Payable (On farm or forestry land)', ''),
    (11, 'Liabilities', 'Long-Term Liabilities', '2500 Long-Term Liabilities',
     '2520 Long-Term Loans Payable (For equipment, vehicles, land improvements)', ''),
    (11, 'Liabilities', 'Long-Term Liabilities', '2500 Long-Term Liabilities',
     '2530 Lease Obligations (Long-term equipment or land leases)', ''),

    # Equity
    (11, 'Equity', 'Shareholders\' Equity', '3000 Shareholders\' Equity', 'Shareholders\' equity account', 'note'),
    (11, 'Equity', 'Shareholders\' Equity', '3000 Shareholders\' Equity', '3010 Common Stock', 'Common stock account'),
    (11, 'Equity', 'Shareholders\' Equity', '3000 Shareholders\' Equity', '3020 Preferred Stock', 'stock account'),
    (11, 'Equity', 'Shareholders\' Equity', '3000 Shareholders\' Equity', '3030 Additional Paid-In Capital',
     'stock account'),

    (11, 'Equity', 'Retained Earnings', '3100 Retained Earnings', '', ''),
    (11, 'Equity', 'Retained Earnings', '3100 Retained Earnings', '3110 Retained Earnings (Prior years profit)',
     'Retained earnings account'),
    (11, 'Equity', 'Retained Earnings', '3100 Retained Earnings', '3120 Current Year Earnings',
     'Retained earnings account'),

    (11, 'Equity', 'Dividends', '3200 Dividends', '', ''),
    (11, 'Equity', 'Dividends', '3200 Dividends', '3210 Dividends Declared', ''),
    (11, 'Equity', 'Dividends', '3200 Dividends', '3220 Dividends Paid', ''),

    # Revenue
    (11, 'Revenue', 'Agricultural Revenue', '4000 Agricultural Revenue', 'Agricultural revenue account', 'note'),
    (11, 'Revenue', 'Agricultural Revenue', '4000 Agricultural Revenue', '4010 Crop Sales',
     'Crop sales revenue account'),

    (11, 'COGS', 'Direct Material Costs', '5000 Direct Material Costs', 'Direct material costs account', 'note'),
    (11, 'COGS', 'Direct Material Costs', '5000 Direct Material Costs', '5010 Seeds', 'Seeds costs'),

    # Operating Expenses d
    (11, 'Operating Expenses', 'Administrative Expenses', '6000 Administrative Expenses',
     'Administrative expenses account', 'note'),
    (11, 'Operating Expenses', 'Administrative Expenses', '6000 Administrative Expenses', '6010 Office Supplies',
     'Office supplies expenses account'),

    # Non-Operating Income and Expenses
    (11, 'Non-Operating Income and Expenses', 'Gains and Losses', '7000 Gains and Losses', 'Gains and losses account',
     'note'),

    # Taxes
    (11, 'Taxes', 'Income Taxes', '8000 Income Taxes', 'Income taxes account', 'note'),

    # Other Accounts
    (11, 'Other Accounts', 'Miscellaneous Accounts', '9000 Miscellaneous Accounts', 'Miscellaneous', ''),
]

naics_data = [
    (11, 'Agriculture, Forestry, Fishing and Hunting', 0, '', 0, ''),
    (11, 'Agriculture, Forestry, Fishing and Hunting', 111, 'Crop Production (e.g., farms, vineyards)', 0, ''),
    (11, 'Agriculture, Forestry, Fishing and Hunting', 112, 'Animal Production', 0, ''),
    (11, 'Agriculture, Forestry, Fishing and Hunting', 113, 'Forestry and Logging', 0, ''),
    (11, 'Agriculture, Forestry, Fishing and Hunting', 114, 'Fishing, Hunting, and Trapping', 0, ''),

    (21, 'Mining, Quarrying, and Oil and Gas Extraction', 0, '', 0, ''),
    (22, 'Utilities', 0, '', 0, ''),
    (23, 'Construction', 0, '', 0, ''),
    (23, 'Construction', 231, 'Residential Home Builders', 0, ''),
    (23, 'Construction', 232, 'Commercial Contractors', 0, ''),
    (23, 'Construction', 233, 'Specialty Trade Contractors', 0, ''),

    (31, 'Manufacturing', 0, '', 0, ''),
    (31, 'Manufacturing', 311, 'Food Manufacturing', 0, ''),

    (42, 'Wholesale Trade', 0, '', 0, ''),
    (42, 'Wholesale Trade', 423, 'groceries', 0, ''),
    (42, 'Wholesale Trade', 424, 'paper products', 0, ''),

    (44, 'Retail Trade', 0, '', 0, ''),
    (44, 'Retail Trade', 441, 'Motor Vehicle and Parts Dealers', 0, ''),
    (44, 'Retail Trade', 442, 'Furniture and Home Furnishings Stores', 0, ''),
    (44, 'Retail Trade', 443, 'Electronics and Appliance Stores', 0, ''),
    (44, 'Retail Trade', 444, 'Grocery Stores', 0, ''),
    (44, 'Retail Trade', 445, 'Clothing and Clothing Accessories Stores', 0, ''),
    (44, 'Retail Trade', 446, 'Hardware Stores', 0, ''),
    (44, 'Retail Trade', 447, 'Bookstores', 0, ''),
    (44, 'Retail Trade', 448, 'E-Commerce Retailers', 0, ''),

    (48, 'Transportation and Warehousing', 0, '', 0, ''),
    (48, 'Transportation and Warehousing', 481, 'Postal Service and Couriers', 0, ''),
    (48, 'Transportation and Warehousing', 482, 'Moving Companies', 0, ''),
    (48, 'Transportation and Warehousing', 483, 'Tax Services', 0, ''),
    (48, 'Transportation and Warehousing', 484, 'Freight Forwarding Companies', 0, ''),

    (51, 'Information', 0, '', 0, ''),
    (52, 'Finance and Insurance', 0, '', 0, ''),
    (52, 'Finance and Insurance', 521, 'Insurance Agencies', 0, ''),

    (53, 'Real Estate and Rental and Leasing', 0, '', 0, ''),
    (53, 'Real Estate and Rental and Leasing', 531, 'Real estate agencies', 0, ''),
    (53, 'Real Estate and Rental and Leasing', 532, 'Commercial Real Estate Agencies', 0, ''),
    (53, 'Real Estate and Rental and Leasing', 533, 'Property management Residential', 0, ''),
    (53, 'Real Estate and Rental and Leasing', 534, 'Real Estate Investment Trusts (REITs)', 0, ''),
    (53, 'Real Estate and Rental and Leasing', 535, 'Car rentals', 0, ''),
    (53, 'Real Estate and Rental and Leasing', 536, 'Machinery leasing', 0, ''),

    (54, 'Professional, Scientific, and Technical Services', 0, '', 0, ''),
    (54, 'Professional, Scientific, and Technical Services', 541, 'Legal Services', 0, ''),
    (54, 'Professional, Scientific, and Technical Services', 542, 'Accounting, Tax Preparation, Bookkeeping', 0, ''),
    (54, 'Professional, Scientific, and Technical Services', 543, 'Marketing Agencies', 0, ''),
    (54, 'Professional, Scientific, and Technical Services', 544, 'IT Consulting Firms', 0, ''),
    (54, 'Professional, Scientific, and Technical Services', 545, 'Architectural, Engineering, and Related Services', 0,
     ''),
    (54, 'Professional, Scientific, and Technical Services', 546, 'Management Consulting Services', 0, ''),
    (54, 'Professional, Scientific, and Technical Services', 547, 'Scientific Research and Development', 0, ''),
    (54, 'Professional, Scientific, and Technical Services', 548, 'Technology Services', 0, ''),
    (54, 'Professional, Scientific, and Technical Services', 548, 'Technology Services', 5481,
     'Software Development Firms'),
    (54, 'Professional, Scientific, and Technical Services', 548, 'Technology Services', 5482, 'IT Support Services'),
    (54, 'Professional, Scientific, and Technical Services', 548, 'Technology Services', 5483,
     'Cloud Hosting Providers'),
    (54, 'Professional, Scientific, and Technical Services', 548, 'Technology Services', 5484, 'IT Consulting Firms'),
    (54, 'Professional, Scientific, and Technical Services', 548, 'Technology Services', 5485, 'Data Centers'),

    (56, 'Administrative and Support and Waste Management and Remediation Services', 0, '', 0, ''),
    (56, 'Administrative and Support and Waste Management and Remediation Services', 561, 'Employment Services', 0, ''),
    (56, 'Administrative and Support and Waste Management and Remediation Services', 562, 'Security Services', 0, ''),

    (61, 'Educational Services', 0, '', 0, ''),
    (61, 'Educational Services', '611', 'Private Schools', 0, ''),
    (61, 'Educational Services', '612', 'Technical and Trade Schools', 0, ''),
    (61, 'Educational Services', '613', 'Online Educational Platforms', 0, ''),
    (61, 'Educational Services', '614', 'Tutoring Services', 0, ''),

    (62, 'Health Care and Social Assistance', 0, '', 0, ''),
    (62, 'Health Care and Social Assistance', 621, 'Ambulatory Health Care Services', 0, ''),
    (62, 'Health Care and Social Assistance', 622, 'Nursing and Residential Care Facilities', 0, ''),
    (62, 'Health Care and Social Assistance', 623, 'Social Assistance', 0, ''),

    (71, 'Arts, Entertainment, and Recreation', 0, '', 0, ''),
    (71, 'Arts, Entertainment, and Recreation', 711, 'Performing Arts Companies', 0, ''),
    (71, 'Arts, Entertainment, and Recreation', 712, 'Museums, Art Galleries, Historical Sites', 0, ''),
    (71, 'Arts, Entertainment, and Recreation', 713,
     'Amusement, Gambling, and Recreation Industries (e.g., fitness centers, amusement parks)', 0, ''),
    (71, 'Arts, Entertainment, and Recreation', 714, 'Film Production Companies', 0, ''),
    (71, 'Arts, Entertainment, and Recreation', 715, 'Music Recording Studios', 0, ''),

    (72, 'Accommodation and Food Services', 0, '', 0, ''),
    (72, 'Accommodation and Food Services', 721, 'Restaurants and Other Eating Places', 0, ''),
    (72, 'Accommodation and Food Services', 722, 'Catering Services', 0, ''),

    (81, 'Other Services (except Public Administration)', 0, '', 0, ''),
    (81, 'Other Services (except Public Administration)', 811, 'Repair and Maintenance', 0, ''),
    (81, 'Other Services (except Public Administration)', 812, 'Personal Care Services', 0, ''),

    (92, 'Public Administration', 0, '', 0, ''),

    (93, 'NPO', 0, '', 0, ''),
    (93, 'NPO', '931', 'Charitable Organizations', 0, ''),
    (93, 'NPO', '932', 'Religious Organizations', 0, ''),
    (93, 'NPO', '933', 'Foundations', 0, ''),
    (93, 'NPO', '934', 'Environmental Advocacy Group', 0, ''),
]
