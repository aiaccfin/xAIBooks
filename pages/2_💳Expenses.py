import streamlit as st
from app.utils import streamlit_components
streamlit_components.streamlit_ui('🦣 Dashboard')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2= st.tabs(["Receipts/Bills", "Reimbursement"])

if __name__ == "__main__":

    st.image('./images/expenses.jpeg')