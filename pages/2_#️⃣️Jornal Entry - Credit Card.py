import streamlit as st
from streamlit_extras.stateful_button import button

from apps.db.db_postgres_aws import PGHandler
from apps.utils import streamlit_components

streamlit_components.streamlit_ui('🦣 Dashboard for Accountant')
pg_handler = PGHandler()
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(['Step 1: Check New Email',  "Step 2: Vendor and COA", 'Step3: Book Journal Entries','Step 4: Show Journals'])

with tab2:
    if button("Process for Vendor and COA?", key='cc21'):
        df = pg_handler.get_and_update_(table_name='bk_transaction', biz_entity_id=801, case = 'vendor_and_coa')

    if button("Show Processed Vendor and COA?", key='cc22'):
        df = pg_handler.show_transactions(table_name='bk_transaction')
        st.dataframe(df)

with tab3:
    if button("Book Journals", key='cc24'):
        df = pg_handler.get_and_update_(table_name='bk_transaction', biz_entity_id=801, case = 'book_journals', biz_status  = 's2_coa')
    st.success('done')

with tab1:
    df = pg_handler.email_new_transactions_process()
    st.dataframe(df)

with tab4:
    if button("Show Journals", key='cc245'):
        df = pg_handler.show_transactions(table_name='bk_transaction', biz_entity_id=801, biz_status ='s3_book_journals')
        st.dataframe(df)
    st.success('done')

