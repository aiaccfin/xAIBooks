import streamlit as st
from apps.utils import streamlit_components
streamlit_components.streamlit_ui('🦣 Dashboard')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["AP", "AR", "Payment Processing"])


if __name__ == "__main__":

    st.image('./images/payments.jpeg')