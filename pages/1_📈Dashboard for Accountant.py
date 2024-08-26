import streamlit as st
from streamlit_extras.stateful_button import button

from app.utils import streamlit_components
# from app.data_entry import email_processing
import app.utils as utils
# app.utils.streamlit_components.streamlit_ui('🦣 Dashboard for Accountant')
streamlit_components.streamlit_ui('🦣 Dashboard for Accountant')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data Entry: Bank Statement", "Data Entry: Receipt", "Data Entry: Scan", "Data Entry: Manual", "DB Structure"])

# with tab2:
#     if button("Extract from Email", key="button2"):    email_processing.email_extraction()
#
# with tab1:
#     pass;