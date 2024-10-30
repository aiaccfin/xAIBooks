import streamlit as st
from streamlit_extras.stateful_button import button

import config.config as cfg
from apps.utils import streamlit_components
from apps.db.db_postgres_aws import PGHandler

streamlit_components.streamlit_ui('🦣 BizEntity Setup')
pg_handler = PGHandler()
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Basic","Tax" , "Financial", "vendor", "coa", "client"])

with tab1:
    df = pg_handler.show_general(table_name='biz_entity', biz_id=cfg.biz_id)
    biz_industry = df.iloc[0]['biz_industry']
    biz_industry_id = df.iloc[0]['biz_industry_id']
    st.dataframe(df)


with tab2:
    df_tax = df[['biz_name','biz_base_currency', 'biz_fiscal_year', 'biz_tax_setting']]
    st.dataframe(df_tax)


with tab3:
    df = pg_handler.show_general(table_name='biz_entity', biz_id=cfg.biz_id, module = 'biz_entity_setup_financial')
    # df_fin = df[['biz_name','biz_base_currency', 'biz_default_payment_term', 'biz_primary_bank_id']]
    st.dataframe(df)


with tab4:
    df = pg_handler.show_general(table_name='vendors', biz_id=cfg.biz_id, module = 'vendors')
    st.dataframe(df)

with tab5:
    st.info('System automaically match COA with your business category of: \n\n ' + biz_industry)
    df = pg_handler.show_general(table_name='biz_coa', biz_id=cfg.biz_id, module = 'biz_coa')
    st.dataframe(df)

    if button("Click to restore to factory settings, your change will not be able to recovered.", key='coa41'):
        pg_handler.copy_default_coa_to_biz(biz_type=biz_industry_id, biz_id=cfg.biz_id)


with tab6:
    df = pg_handler.show_general(table_name='clients', biz_id=cfg.biz_id, module = 'clients')
    st.dataframe(df)
