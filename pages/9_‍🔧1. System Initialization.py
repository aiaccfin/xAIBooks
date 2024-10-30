import streamlit as st
from streamlit_extras.stateful_button import button
from apps.utils import streamlit_components

from apps.db.db_postgres_aws import PGHandler

streamlit_components.streamlit_ui('🦣 Dashboard')
pg_handler = PGHandler()
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Default COA", "Business Types and Industry Categories", "System Initialization"])

with tab2:
    if button("Show?", key="button91"):
        df = pg_handler.get_naics()
        st.dataframe(df)
    if button("ReLoad NAICS?", key="button97"):
        # pg_handler.load_default_naics()
        st.success('System is ready for use. This function need only run once.')


with tab3:
    if button("create tables?", key="button32"):
        pg_handler.create_table_if_not_exists()
        st.success('System is ready for use. This function need only run once.')


with tab1:
    if button("List COA?", key="button931"):
        df = pg_handler.get_default_coa()
        st.dataframe(df)

    if button("Load Default COA to DB?", key="button31"):
        # pg_handler.load_default_coa()
        st.success('System is ready for use. This function need only run once.')


