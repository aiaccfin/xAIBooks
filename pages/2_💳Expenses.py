import streamlit as st
from app.utils import streamlit_components
from app.db.db_postgres import PGHandler

streamlit_components.streamlit_ui('🦣 Expenses')
pg_handler = PGHandler()
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3= st.tabs(["Vendors", "Bills and Payments", "Reimbursement"])

with tab1:
    business_id = 801
    df = pg_handler.get_vendor_list(business_id)
    df.columns = ['Business ID', 'Vendor ID', 'Vendor Name','Vendor Code', 'Tax Type', 'vendor_type', 'vendor_category', 'credit_limit', 'threshold']
    st.dataframe(df)

with tab2:
    business_id = 801
    vendor_id = 5
    vendor_name = 'Walmart'
    transaction_id = 32

    st.subheader('Vendor Information')
    df_vendor = pg_handler.get_vendor_info(business_id=business_id, vendor_name=vendor_name)
    df_vendor.columns = ['Me', 'Vendor_ID', 'Vendor Name','Info', 'Vendor Code']
    st.dataframe(df_vendor)

    st.subheader('Bills of '+vendor_name )
    df = pg_handler.get_bills(vendor_name)
    df.columns = ['transaction id', 'BizEntity', 'Issue Date', 'Description','Amt', 'Due Date', 'Paid Date']
    st.dataframe(df)

    st.subheader('Payments of transaction 32')
    df = pg_handler.get_payments(business_id=business_id, vendor_id=vendor_id, transaction_id=transaction_id)
    df.columns = ['transaction id', 'Pay Date', 'Amt', 'Payment Method','Status', 'Note']

    st.dataframe(df)


with tab3: st.warning('under construction...')