import streamlit as st
from streamlit_extras.stateful_button import button
from app.utils import streamlit_components

from app.db.db_postgres import PGHandler

streamlit_components.streamlit_ui('🦣 Dashboard')
pg_handler = PGHandler()
# -----------------------------------------------------------------------------------------------------------
tab1, tab2 = st.tabs(
    ["coa",  "init"])

with tab2:
    if button("Initialization?", key="button3"):
        st.success('System is ready for use. This function need only run once.')


with tab1:
    if button("COA?", key="button31"):
        pg_handler.save_coa()
        st.success('System is ready for use. This function need only run once.')
