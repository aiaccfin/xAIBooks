import streamlit as st

from streamlit_extras.stateful_button import button
from app.utils import (streamlit_components,)

streamlit_components.streamlit_ui('🐬🦣 xAI Books 🍃🦭')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Email Rule", "", "", ""])

with tab1:
    st.write('''

    ##### Final Goal: 
    Automated Accounting System (like Quickbook without human-interaction)

    ##### Tier1 Scope: 
    1. Datasource: structured PDF and CSV.
    2. Customer is enterprise, direct client. Agents/Accoutants will be considered in Tier2.

    ##### Input: 
    Bank Statement, Invoice, Receipt 

    ##### Output: 
        1. Vendor, Customer, COA
        2. AP/AR
        3. Income Statement
        4. Cash Flow
        5. Reconcil
        6. Tax 
        7. Reporting

    ''')
    st.image('./images/dashboard.jpeg')


with tab2:
    st.write('''
        1. Each login is associated with one Customer ID, `n:1` (for agents, Customer ID will be an array)
        2. Each customer has a unique Customer ID (for example: `xaibooks`.) 
        3. Each customer ID `xaibooks` has an email associated with it (`xaibooks@outlook.com`)
        4. Receipt/Invoice/Bank Statement must be sent to this email to be extracted and interpreted.
        5. Email extraction will be stored:
            - Receipt: `./data/cusotmerID/receipt`
            - Invoice: `./data/customerID/invoice`
            - Bank Statement: `./data/customerID/bs`
        6. Only retrieve emails from INBOX
        7. The retrieved emails will be moved to RETRIEVED Folder and keep them as is.
    ''')

