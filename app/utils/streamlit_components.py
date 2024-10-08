import streamlit as st
from streamlit_extras.stateful_button import button

def streamlit_ui(main_title):
    st.set_page_config(page_title='xAI Books '+main_title, page_icon="🚀", )
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
    if "login_status" not in st.session_state:
        st.session_state.login_status = False

    if not st.session_state.login_status:

        password = st.text_input("Enter password", type="password")
        if st.button("Login"):
            if password == st.secrets["password"]:
                st.session_state.login_status = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid password, try again!")
        st.warning("You must log in to access the app")
        st.stop()

