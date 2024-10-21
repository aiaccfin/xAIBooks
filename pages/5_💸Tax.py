import streamlit as st
from apps.utils import streamlit_components
streamlit_components.streamlit_ui('🦣 Dashboard')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Sales Tax", "Income Tax", "Payroll Tax"])
if __name__ == "__main__":

    st.image('./images/timetracking.jpeg')