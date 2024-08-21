import streamlit as st
from ..utils.tools import time_it


class ChatUI:
    def __init__(self, db_handler, llm_handler, vector_or_others):
        self.db_handler = db_handler
        self.llm_handler = llm_handler
        self.vector_or_others = vector_or_others

    @time_it(label='ChatGPT ')
    def respond_contents(self, message):
        return self.llm_handler.get_response_from_llm(message)

    @time_it(label='SQL Execution ')
    def result(self, respond_contents):
        return self.db_handler.execute_sql(respond_contents)

    def send_message(self, message):
        
        respond_contents = self.respond_contents(message)
        
        result = self.result(respond_contents)
        
        result = result.replace("),", "),  \n")
        return {"message": respond_contents + "\n\n ###### Result: ###### \n\n" + result}

    def run(self):
        """
        Runs the chat UI, displaying messages and handling user input.
        """
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("⌨️ ask me "):
            st.chat_message("user").markdown(prompt)            # 1.Display user message in chat message container

            st.session_state.messages.append(
                {"role": "user", "content": prompt})            # 2. Add user message to chat history

            response = self.send_message(prompt)["message"]     # 3. Get message from ChatGPT
            with st.chat_message("assistant"):
                st.info(response)                           # 4. Display message from ChatGPT

            st.session_state.messages.append(
                {"role": "assistant", "content": response})     # 5. keep history
