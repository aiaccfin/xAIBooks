import streamlit as st
from apps.utils import streamlit_components

from apps.db.db_postgres import PGHandler

streamlit_components.streamlit_ui('🦣 BizEntity Setup')
pg_handler = PGHandler()
# -----------------------------------------------------------------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Basic","Tax and Financial", "vendor", "coa", "client"])

with tab1:
    df = pg_handler.get_business_basic(801)
    df.columns = ['businessID', 'Name', 'Phone', 'Country', 'Address', 'Industry', 'Info']
    st.dataframe(df)


with tab2:
    df = pg_handler.get_business_fin(801)
    df.columns = ['businessID', 'Name', 'Base Currency', 'Fiscal Year End', 'tax_setting', 'default_payment_term', 'Accounting System','bank 1', 'bank 2', 'bank 3' ]
    st.dataframe(df)

with tab3:
    df = pg_handler.get_vendor_list()
    df.columns = ['Business ID', 'Vendor ID', 'Vendor Name', 'Vendor Code', 'Accounting System', 'Vendor Type', 'Vendor Category', 'Credit Limit', 'Threshold' ]
    st.dataframe(df)

with tab4:
    df = pg_handler.get_coa_list()
    df.columns = ['Business ID', 'Vendor ID', 'COA Category', 'COA Sub-Category', 'COA']
    st.dataframe(df)


with tab5:
    df = pg_handler.get_client_list()
    df.columns = ['Business ID', 'Client ID', 'Client Name', 'Client Type', 'Category', 'credit_limit', 'payment_method', 'credit_term']
    st.dataframe(df)
