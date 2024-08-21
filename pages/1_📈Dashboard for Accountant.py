import streamlit as st

from app.utils import streamlit_components
from app.data_entry import email_processing
streamlit_components.streamlit_ui('🦣 Dashboard for Accountant')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Email Rule","Data Entry: Email", "Data Entry: Scan", "Data Entry: Manual", "DB Structure"])

with tab2:  email_processing.email_extraction()






with tab1:
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