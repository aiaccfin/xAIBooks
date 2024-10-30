import pandas as pd
import streamlit as st
from apps.utils import streamlit_components
from apps.db.db_postgres_aws import PGHandler

streamlit_components.streamlit_ui('🦣 Invoice Management')
pg_handler = PGHandler()
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Invoices", "Product Sales", "Other Revenue"])

with tab1:
    biz_id = 801
    invoice_number = 'C10303'

    df = pg_handler.get_invoice(biz_id=biz_id, invoice_number=invoice_number)

    st.subheader(f'Invoice Number: {df["invoice_number"].iloc[0]}')
    # st.subheader(f'Recuring? {df["invoice_recurring"].iloc[0]}')
    st.markdown(f"<h6>Recurring? <span style='color:red;'>{df['invoice_recurring'].iloc[0]}</span></h6>",unsafe_allow_html=True)

    st.info(f'biz ID:{df["biz_id"].iloc[0]} | biz Name: {df['biz_name'].iloc[0]}')
    st.info(f'Customer ID:{df['customer_name'].iloc[0]} | client name: {df['client_name'].iloc[0]} | Address:{df['client_address'][0]} | Payment Method: {df['client_payment_method'].iloc[0]}')
    df_item = pd.DataFrame(df, columns = ['item_description', 'item_quantity', 'item_unit_price', 'item_tax_rate','item_tax', 'item_amount'])
    st.dataframe(df_item)

    st.subheader(f'Total: ${df['invoice_total_amount'].iloc[0]:,.2f}')
    st.info(f'Issue Date:   {df['issue_date'].iloc[0]}  |  Due Date:{df['due_date'].iloc[0]}')
    st.error(f'Status:   {df['status'].iloc[0]}')
