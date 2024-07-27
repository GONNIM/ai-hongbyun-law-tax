import streamlit as st  # type: ignore
import get_user_info
import history
import sidebar
import chat

from logger import print_and_log


st.set_page_config(page_title="소득세법 챗봇", page_icon="⚖️")


if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = True

if 'user_key' not in st.session_state:
    st.session_state.user_key = None

if 'session_id' not in st.session_state:
    st.session_state.session_id = None
    print_and_log(f"app.py > session_id not in st.session_state)")

if 'history_list' not in st.session_state:
    st.session_state.history_list = []

if 'selected_history' not in st.session_state:
    st.session_state.selected_history = []


def main():
    if st.session_state.selected_history == []:
        history.load_history_list()

    user_key = get_user_info.get_user_info()
    # print_and_log(f"main() > get_user_info.get_user_info() > User Key: {user_key}")

    # 사이드바 파일 호출
    sidebar.show_sidebar()

    # 메인 파일 호출
    chat.show_main()


if __name__ == "__main__":
    main()
