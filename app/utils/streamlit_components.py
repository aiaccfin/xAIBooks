import streamlit as st


def streamlit_ui(main_title):
    st.set_page_config(page_title='AI Accounting 👋', page_icon="💯", ),
    st.title(main_title)  # not accepting default

    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://omnidevx.netlify.app/logo/XAI_Logo.png);
                background-size: 250px; /* Set the width and height of the image */
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 35px 0px;
            }
        </style>
        """,
                unsafe_allow_html=True,
                )
