
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

my_key_openai = st.secrets["mykey_openai"]

user = os.getenv("user_name")
password = os.getenv("user_password")
dsn = os.getenv("dsn_info")

llm_openai = ChatOpenAI(api_key = my_key_openai, model = "gpt-4o-mini", temperature=0.2, streaming=True)
embeddings = OpenAIEmbeddings(api_key = my_key_openai, model="text-embedding-3-large")


st.set_page_config(page_title="SQL Helper Chatbot", page_icon="🤖", layout="centered")


if "user_info_submitted" not in st.session_state:
    st.session_state.user_info_submitted = False

if not st.session_state.user_info_submitted:

    with st.form("user_info_form"):
        st.subheader("SQL Developer 💬")

        name = st.text_input("Ad", key='name')
        surname = st.text_input("Soyad", key='surname')
        department = st.text_input("Departament adı", key='department')

        def submit_user_info():
            
            if st.session_state.name and st.session_state.surname and st.session_state.department:
                st.session_state.user_info = {
                    "name": st.session_state.name,
                    "surname": st.session_state.surname,
                    "department": st.session_state.department
                }
                st.session_state.user_info_submitted = True
            else:
                st.warning("Məlumatlarınızı daxil edin")

        submit_button = st.form_submit_button("Daxil ol", on_click=submit_user_info)

        
        if submit_button:
            if name and surname and department:
            
                st.session_state.user_info = {"name": name, "surname": surname, "department": department}
                st.session_state.user_info_submitted = True

            else:
                st.warning("Məlumatlarızı daxil edin")


else:
    st.title("💬 SQL Helper Chatbot")
    st.divider()


    def get_final_prompt(prompt):


        final_prompt = f"""
        Analyze the following SQL Script. Identify performance, security, and style issues.  
        Suggest improvements and provide a corrected version.  
        Explain reasoning concisely. 
        - Modify SQL queries as requested while following best practices.
        - Optimize queries for performance, readability, and efficiency.
        - Detect and correct errors in SQL syntax and logic.
        - Provide clear comments explaining any changes made.
        - Suggest indexing, restructuring, or other improvements when relevant.

        SQL Script: {prompt}
        """
        return final_prompt

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "system", "content": "Your role is to help users modify, optimize, and improve SQL scripts."})

    for message in st.session_state.messages[1:]:
        role = message.get("role", "user")
        avatar = message.get("avatar", "👨🏻" if role == "user" else "🤖")
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message.get("content", ""))

    if prompt := st.chat_input("Sualınızı yazın..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "👨🏻"})
        st.chat_message("user", avatar="👨🏻").markdown(prompt)

        response_text = ""
        with st.chat_message("assistant", avatar="🤖") as assistant_message:
            response_placeholder = st.empty() 

            final_prompt = get_final_prompt(prompt)

            for token in llm_openai.stream(st.session_state.messages + [{"role": "user", "content": final_prompt}]):
                token_content = token.content
                response_text += token_content
                response_placeholder.markdown(response_text) 


            st.session_state.messages.append({"role": "assistant", "content": response_text, "avatar": "🤖"})


   

                