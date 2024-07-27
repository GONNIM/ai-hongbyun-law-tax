import streamlit as st  # type: ignore
import chat
import history

from logger import print_and_log


MAX_SUBJECT_LEN = 15

if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = True

if 'history_list' not in st.session_state:
    st.session_state.history_list = []

if 'selected_history' not in st.session_state:
    st.session_state.selected_history = []

if "delete_history" not in st.session_state:
    st.session_state.delete_history = False


def toggle_sidebar():
    st.session_state.sidebar_open = not st.session_state.sidebar_open


def show_sidebar():
    if st.session_state.sidebar_open:
        if st.session_state.history_list == []:
            history.load_history_list()

        with st.sidebar:
            show_history()


def show_history():
    if st.sidebar.button("New Chat"):
        st.session_state.session_id = None
        st.session_state.history_list = []
        st.session_state.selected_history = []
        st.session_state.message_list = []
        st.rerun()
    
    st.sidebar.divider()

    if st.session_state.history_list:
        st.sidebar.header("History")

        idx = 0
        for item in st.session_state.history_list:
            cols = st.sidebar.columns([3, 1, 1])  # 3:1:1 비율로 세 개의 column을 만든다.
            with cols[0]:
                subject = f"{item['subject']}"
                if len(subject) > MAX_SUBJECT_LEN:
                    subject = subject[:MAX_SUBJECT_LEN] + "..."
                st.subheader(subject)
            with cols[1]:
                session_id = item['session_id']
                s_idx = f"select_{session_id}_{idx}"
                # print_and_log(s_idx)
                clicked = st.button(f"보기", key=s_idx)
                if clicked:
                    st.session_state.selected_history = []
                    st.session_state.message_list = []
                    st.session_state.selected_history = history.load_history(session_id)
                    st.session_state.session_id = session_id
                    selected_history_to_message_list()
                    st.rerun()
            with cols[2]:
                session_id = item['session_id']
                subject = item['subject']
                timestamp = item['timestamp']
                s_idx = f"delete_{session_id}_{idx}"
                clicked = st.button(f"삭제", key=s_idx)
                if clicked:
                    delete_history(session_id, subject, timestamp)                        

            idx += 1


def selected_history_to_message_list():
    if st.session_state.selected_history:
        for history in st.session_state.selected_history:
            st.session_state.message_list.append({"role": "user", "content": history['question']})
            st.session_state.message_list.append({"role": "ai", "content": history['answer']})


@st.experimental_dialog("Would you like to delete the History?")
def delete_history(session_id, subject, timestamp):
    st.write(subject)
    st.write(timestamp)
    if st.button("Delete"):
        history.delete_from_history(session_id)
        st.session_state.session_id = None
        st.session_state.history_list = []
        st.session_state.selected_history = []
        st.session_state.message_list = []
        st.rerun()
