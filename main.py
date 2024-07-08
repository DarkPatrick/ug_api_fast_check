# streamlit_app.py
import streamlit as st
import requests
import datetime
import hashlib
import pytz

def generate_api_key(client_id):
    current_time = datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d:%-H")
    # print(current_time)
    return hashlib.md5(f"{client_id}{current_time}createLog()".encode()).hexdigest()

# Set up the Streamlit application
st.title("Simple API Requestor")

# Input fields for user name and password
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Input field for the request path URL
request_url = st.text_input("Request URL")

# Button to initiate the request
if st.button("Get Response"):
    # Make the request with basic authentication
    try:
        client_id = "test_client"
        # current_time = datetime.datetime.now(pytz.utc).strftime("%Y-%m-%d:%-H")
        # api_key = hashlib.md5(f"{client_id}{current_time}createLog()".encode()).hexdigest()
        api_key = generate_api_key(client_id)
        url = 'https://api.ultimate-guitar.com/api/v1/auth/login'
        headers = {
            'User-Agent': 'UGT_ANDROID/8.8.8.8 (MAGIC_DEVICE; iOS_Android)',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-UG-API-KEY': api_key,
            'X-UG-CLIENT-ID': client_id
        }
        data = {
            'username': username,
            'password': password
        }
        print(data)
        response = requests.put(url, headers=headers, data=data)
        print(response.json())
        # print(response.json()['token'])

        if response.status_code == 200:
            st.success("Request successful!")

            api_key = generate_api_key(client_id)
            token = response.json()['token']
            url = f'https://api.ultimate-guitar.com/api/v1/purchase/promo?token={token}'
            headers = {
                'User-Agent': 'UGT_ANDROID/8.8.8.8 (MAGIC_DEVICE; iOS_Android)',
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-UG-API-KEY': api_key,
                'X-UG-CLIENT-ID': client_id
            }

            data_response = requests.get(f'https://api.ultimate-guitar.com/api/v1/{request_url}?token={token}', headers=headers)

            print(data_response.json())

            json_response = data_response.json()
            st.json(json_response)
        else:
            st.error(f"Request failed with status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# To run this Streamlit app, save this script as `streamlit_app.py`
# and run the following command in your terminal:
# streamlit run streamlit_app.py
