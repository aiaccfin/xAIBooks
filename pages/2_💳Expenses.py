import streamlit as st
from streamlit_extras.stateful_button import button

from apps.utils import streamlit_components
from apps.db.db_postgres_aws import PGHandler

streamlit_components.streamlit_ui('🦣 Expenses')
pg_handler = PGHandler()
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3= st.tabs(["Vendors", "Bills and Payments", "Reimbursement"])

with tab1:
    business_id = 801
    vendor_id = 5
    vendor_name = 'Walmart'
    transaction_id = 32

    st.info('list all the vendors for: ' + str(business_id))
    st.write('clicking vendor will drill down to bills and payments')
    df = pg_handler.get_vendor_list(business_id)
    df.columns = ['Business ID', 'Vendor ID', 'Vendor Name','Vendor Code', 'Tax Type', 'vendor_type', 'vendor_category', 'credit_limit', 'threshold']
    st.dataframe(df)

with tab2:
    st.subheader('Vendor Information')
    df_vendor = pg_handler.get_vendor_info(business_id=business_id, vendor_name=vendor_name)
    df_vendor.columns = ['Me', 'Vendor_ID', 'Vendor Name','Info', 'Vendor Code']
    st.dataframe(df_vendor)

    if button("Show Bills?", key='sb1'):
        st.subheader('Bills of '+vendor_name )
        df = pg_handler.get_bills(vendor_name)
        df.columns = ['transaction id', 'BizEntity', 'Issue Date', 'Description','Amt', 'Due Date', 'Paid Date']
        st.dataframe(df)

        if button("Show Payments?", key='sb12'):
            st.subheader('Payments of transaction 32')
            df = pg_handler.get_payments(business_id=business_id, vendor_id=vendor_id, transaction_id=transaction_id)

            st.dataframe(df)


with tab3: st.warning('under construction...')
