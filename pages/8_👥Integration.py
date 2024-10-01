import streamlit as st
from openai import OpenAI
from app.utils import streamlit_components
from app.llm.openai_api import get_vendor
streamlit_components.streamlit_ui('🦣 Dashboard')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["AS", "Tax Software", "API Documentation"])

if __name__ == "__main__":
    get_vendor("CIRCLE K #20850 MORRISVILLE NC")

    # client = OpenAI()
    #
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo-0125",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {
    #             "role": "user",
    #             "content": "Tell a joke"
    #         }
    #     ]
    # )
    #
    # st.write(completion.choices[0].message)