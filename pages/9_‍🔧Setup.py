import streamlit as st
from streamlit_extras.stateful_button import button

from app.utils import streamlit_components
streamlit_components.streamlit_ui('🦣 Dashboard')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    ["System Initialization", "", ""])

with tab1:
    if button("Initialization?", key="button3"):
        from app.db import db_handler
        db_handler = db_handler.PGHandler()

        db_handler.truncate_table('cc_transactions')
        st.success('System is ready for use. This function need only run once.')
