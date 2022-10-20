import pickle
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

#USER AUTHENTICATION
names = ["Akkshaya Sri", "Swetha Srinivasan"]
usernames = ["asri", "ssrini"]

#Load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.authenticate(names, usernames, hashed_passwords)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Invalid username or password")
if authentication_status == None:
    st.warning("Please enter your username and password")
if authentication_status:
    st.write("Success")
