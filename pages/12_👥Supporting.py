import streamlit as st
from openai import OpenAI
from app.utils import streamlit_components
from app.llm.openai_api import return_vendor
streamlit_components.streamlit_ui('🦣 Dashboard')
# -----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    return_vendor("CIRCLE K #20850 MORRISVILLE NC")

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