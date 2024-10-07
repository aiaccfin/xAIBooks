import streamlit as st
from app.utils import streamlit_components
streamlit_components.streamlit_ui('🦣 Dashboard')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Invoicing Template", "Product Sales", "Other Revenue"])

if __name__ == "__main__":

    st.image('./images/expenses.jpeg')