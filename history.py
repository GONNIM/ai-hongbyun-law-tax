import streamlit as st  # type: ignore
import pandas as pd
import os
import csv
import json
from datetime import datetime
from logger import print_and_log


if 'user_key' not in st.session_state:
    st.session_state.user_key = None

if 'session_id' not in st.session_state:
    st.session_state.session_id = None

if 'selected_history' not in st.session_state:
    st.session_state.selected_history = []

# History File
HISTORY_FILE = 'chatbot_history.json'
HISTORY_CSV_FILE = 'chatbot_history.csv'


# CSV File Initialize
def initialize_csv_file():
    if not os.path.exists(HISTORY_CSV_FILE):
        with open(HISTORY_CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['User Key', 'Session Id', 'Subject', 'Timestamp'])


def save_history_to_csv(user_key, session_id, subject):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(HISTORY_CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_key, session_id, subject, timestamp])


def load_existing_session_ids():
    session_ids = set()
    if os.path.exists(HISTORY_CSV_FILE):
        with open(HISTORY_CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader) # Jump Header
            for row in reader:
                if row:
                    session_ids.add(row[1])
    return session_ids


def is_same_session_id(session_id, existing_session_ids):
    return session_id in existing_session_ids


# Load History List
def load_history_list():
    initialize_csv_file()

    if st.session_state.user_key:
        st.session_state.history_list = []

        if os.path.exists(HISTORY_CSV_FILE):
            with open(HISTORY_CSV_FILE, mode='r') as file:
                reader = csv.reader(file)
                next(reader) # Jump Header
                for row in reader:
                    if row:
                        user_key = row[0]
                        session_id = row[1]
                        subject = row[2]
                        timestamp = row[3]
                        if st.session_state.user_key == user_key:
                            st.session_state.history_list.append({'session_id': session_id, 'subject': subject, 'timestamp': timestamp})


if 'history_list' not in st.session_state:
    load_history_list()


def load_history(target_session_id):
    # Read History
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    selected_history = [item for item in history if item['id'] == target_session_id]
    return selected_history


def save_history(add_history):
    recv_history = []
    recv_history.append(add_history)

    # Read History
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    # Add History
    history.extend(recv_history)
    
    # Save History
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)


# Add History
def add_to_history(session_id, question, answer):
    existing_session_ids = load_existing_session_ids()
    if is_same_session_id(session_id, existing_session_ids):
        print_and_log("add_to_history() > Same history session id detected")
    else:
        print_and_log("add_to_history() > New history session id detected")
        user_key = st.session_state.user_key
        if user_key:
            save_history_to_csv(user_key, session_id, question)

    add_history = {'id': session_id, 'question': question, 'answer': answer} 
    save_history(add_history)


# Delete History
def delete_from_history(session_id):
    delete_history_csv(session_id)
    delete_history_json(session_id)


def delete_history_csv(session_id):
    # Read CSV File
    df = pd.read_csv(HISTORY_CSV_FILE, header=None)
    # Delete Row
    df_filtered = df[df[1] != session_id]
    # Save CSV File
    df_filtered.to_csv(HISTORY_CSV_FILE, index=False, header=False)
    

def delete_history_json(session_id):
    # Read Json
    with open(HISTORY_FILE, 'r') as file:
        data = json.load(file)
    # Delete Target Data
    filtered_data = [item for item in data if item['id'] != session_id]
    # Save Json
    with open(HISTORY_FILE, 'w') as file:
        json.dump(filtered_data, file, indent=4)
