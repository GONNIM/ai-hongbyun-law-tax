import streamlit as st  # type: ignore
import json
import uuid
import history

from dotenv import load_dotenv
from llm import get_ai_response
from logger import print_and_log


def start_session():
    session_id = str(uuid.uuid4())
    st.session_state.session_id = session_id
    st.session_state.message_list = []
    st.session_state.history = []
    return session_id


def end_session():
    if 'session_id' in st.session_state:
        print_and_log(f"Session {st.session_state.session_id} ended.")
        del st.session_state.session_id
        del st.session_state.message_list


# 메인 함수
def show_main():
    st.title("⚖️ 소득세법 챗봇")

    if st.session_state.selected_history == []:
        caption = "무엇이든 물어보세요! 소득세법에 관한 모든 것을 답변해 드립니다."
        st.caption(caption)

        load_dotenv()

        if st.session_state.session_id == None:
            session_id = start_session()
            print_and_log(f"chat.py > Session {session_id} started. (session_id == None)")

        if 'message_list' not in st.session_state:
            session_id = start_session()
            print_and_log(f"chat.py > Session {session_id} started. (message_list)")
        
        for message in st.session_state.message_list:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        placeholder = "소득세에 관련된 궁금한 내용들을 말씀해 주세요!"
        if user_question := st.chat_input(placeholder=placeholder):
            with st.chat_message("user"):
                st.write(user_question)
            st.session_state.message_list.append({"role": "user", "content": user_question})

            with st.spinner("답변을 생성하는 중입니다"):
                ai_response = get_ai_response(user_question)
                with st.chat_message("ai"):
                    ai_message = st.write_stream(ai_response)
                st.session_state.message_list.append({"role": "ai", "content": ai_message})
                history.add_to_history(st.session_state.session_id, user_question, ai_message)
                history.load_history_list()
    else:
        caption = f"History: {st.session_state.session_id}"

        if st.session_state.history_list:
            for list in st.session_state.history_list:
                session_id = list['session_id']
                if session_id == st.session_state.session_id:
                    timestamp = list['timestamp']
                    caption = f"History: {timestamp}"
                    break

        st.caption(caption)

        for message in st.session_state.message_list:
            with st.chat_message(message["role"]):
                st.write(message["content"])
