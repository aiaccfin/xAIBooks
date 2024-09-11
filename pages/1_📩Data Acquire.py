from app.utils import streamlit_components
from streamlit_extras.stateful_button import button
from app.data_entry import email_processing, pdf_processing

streamlit_components.streamlit_ui('🦣 Check Email for Statements, Receipts, and Invoices')

# -----------------------------------------------------------------------------------------------------------
if button("Extract from Email ?", key="button3"):
    email_processing.email_extraction()
