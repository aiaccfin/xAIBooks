import streamlit as st


def main_intro():
    st.write('''

    #### Final Goal: 
    Automated Accounting System (like Quickbook without human-interaction)
    
    #### Tier1 Scope: 
    1. Datasource: structured PDF and CSV.
    2. Customer is enterprise, direct client. Agents/Accoutants will be considered in Tier2.

    #### Input: 
    Bank Statement, Invoice, Receipt 
    
    #### Output: 
        1. Vendor, Customer, COA
        2. AP/AR
        3. Income Statement
        4. Cash Flow
        5. Reconcil
        6. Tax 
        7. Reporting

    ''')
    st.image('./images/dashboard.jpeg')
