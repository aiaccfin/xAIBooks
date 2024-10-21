import pandas as pd
import streamlit as st
from streamlit_extras.stateful_button import button

from apps.utils import streamlit_components

streamlit_components.streamlit_ui('🦣 Workflow Diagram')

# -----------------------------------------------------------------------------------------------------------
st.image('./images/workflow.png')
st.error('1. front end: Showing the whole Accounting Process ...')
st.error('2. system design: clarify # of Red Flagged unfinished spots')
st.error('3. front end: add links to the Lower Portion')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Trial Balance", "General Ledger", "Vendor List", "Transactions", "ChatBot"])

with tab1:
    data = list(mongo_db.collection_cc.find({}, {'_id': 0, 'COA': 1, 'amount': 1}))
    df = pd.DataFrame(data)
    tb = df.groupby('COA').sum().reset_index()

    tb['Debit'] = tb['amount'].apply(lambda x: x if x > 0 else 0)  # Show negative amounts as positive in Debit
    tb['Credit'] = tb['amount'].apply(lambda x: x if x < 0 else 0)  # Show positive amounts in Credit

    tb['Debit'] = tb['Debit'].apply(lambda x: f"{x:.2f}" if x != 0 else "-")  # Two decimals or "-"
    tb['Credit'] = tb['Credit'].apply(lambda x: f"{x:.2f}" if x != 0 else "-")  # Two decimals or "-"

    tb = tb.drop(columns=['amount'])

    st.subheader('Trial Balance')
    st.error('front end add link to GL to be interactive')
    st.table(tb)

with tab2:
    if button("General Ledger", key="button12"):

        data = list(mongo_db.collection_cc.find({}, {'_id': 0, 'date': 1, 'description': 1, 'COA': 1, 'amount': 1}))
        df = pd.DataFrame(data)

        df['Debit'] = df['amount'].apply(lambda x: -x if x < 0 else 0)  # Show negative amounts as positive in Debit
        df['Credit'] = df['amount'].apply(lambda x: x if x > 0 else 0)  # Show positive amounts in Credit

        df = df.drop(columns=['amount'])

        df['Debit'] = df['Debit'].apply(lambda x: f"{x:.2f}" if x != 0 else "-")  # Two decimals or "-"
        df['Credit'] = df['Credit'].apply(lambda x: f"{x:.2f}" if x != 0 else "-")  # Two decimals or "-"

        df = df.sort_values(by=['COA', 'date'])
        coa_list = df['COA'].unique()
        for coa in coa_list:
            st.subheader(f"`{coa}`")
            st.dataframe(df[df['COA'] == coa])

with tab3:
    if button("Show Vendor Information ?", key="button13"):
        vendors = mongo_db.collection_vendor.find()
        for vendor in vendors:
            st.write(f"**Vendor Name**: {vendor['name']}")
            st.write(f"**Business Information**: {vendor['information']}")
            st.divider()

with tab4:
    if button("Show Credit Card Transactions ?", key="button14"):
        data = list(mongo_db.collection_cc.find())
        df = pd.DataFrame(data)
        df.drop(columns=['_id', 'description'], inplace=True)
        st.dataframe(df)

with tab5:
    st.error('''
        1. Data Source? Who provide Data Source and validate?
        2. User case.
    
    ''')
