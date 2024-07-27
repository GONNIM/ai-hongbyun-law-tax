import streamlit as st  # type: ignore
import os
import csv
import hashlib
import platform
import requests
from getmac import get_mac_address # type: ignore
from datetime import datetime
from logger import print_and_log


# CSV File
CSV_FILE = 'user.csv'


# CSV File Initialize
def initialize_csv_file():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['User Key', 'Generated Time', 'Device Info', 'Location'])


# Get System Info
def get_system_info():
    # MAC Address
    mac_address = get_mac_address()

    # CPU ID
    cpu_id = ""
    if platform.system() == "Windows":
        cpu_id = os.popen("wmic cpu get processorid").read().strip().split('\n')[1]
    elif platform.system() == "Linux":
        cpu_id = os.popen("cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2").read().strip()
    elif platform.system() == "Darwin":
        cpu_id = os.popen("sysctl -n machdep.cpu.brand_string").read().strip()

    system_info = f"{mac_address}-{cpu_id}"
    return system_info


# Generate Unique Key
def generate_unique_key(system_info):
    unique_key = hashlib.sha256(system_info.encode()).hexdigest()
    return unique_key


# Load Existing Key
def load_existing_keys():
    existing_keys = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader) # 헤더 건너뛰기
            for row in reader:
                existing_keys.add(row[0])
    return existing_keys


# Check Same User
def is_same_user(new_key, existing_keys):
    return new_key in existing_keys


# Save Key
def save_key_to_csv(unique_key, system_info, user_location):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([unique_key, timestamp, system_info, user_location])


# Get Location
def get_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        return data['city'] + ', ' + data['country']
    except:
        return "Unknown"


def get_user_info():
    initialize_csv_file()
    
    system_info = get_system_info()
    # print_and_log(f"get_user_info() > System Info: {system_info}")

    user_location = get_location()

    # Generate Unique Key
    new_key = generate_unique_key(system_info)
    
    # Load Unique Key
    existing_keys = load_existing_keys()
    
    if is_same_user(new_key, existing_keys):
        print_and_log("get_user_info() > Same user detected")
    else:
        print_and_log("get_user_info() > New user detected")
        save_key_to_csv(new_key, system_info, user_location)
    
    user_key = new_key
    st.session_state.user_key = user_key
    return user_key
