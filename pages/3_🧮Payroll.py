import streamlit as st
from apps.utils import streamlit_components
streamlit_components.streamlit_ui('🦣 Dashboard')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Employee List", "Timesheet Recording", ""])

if __name__ == "__main__":

    st.image('./images/estimates.jpeg')