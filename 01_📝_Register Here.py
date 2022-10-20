import streamlit as st
import requests
from streamlit_lottie import st_lottie
import pandas as pd
import csv


st.set_page_config(page_title="Rise - Registration", page_icon=":office:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#df = pd.read_csv("D:\COLLEGE\YEAR V\SEM IX\MINOR PROJECT\proj\users.csv")
#df = pd.DataFrame(columns=['email','pwd','f_name', 'l_name', 'age','gender', 'skills', 'experience', 'exp', 'sear', 'location', 'company'])
#LOAD ASSETS
lottie_coding = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_pprxh53t.json")
lottie_success = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_t58qlnnx.json")


#HEADER
with st.container():
    st.subheader("Create an account to continue.." )
    st.title("User Registration")
def form():
    st.write("Registration")
    with st.form(key = "Information form"):
        email = st.text_input("Email Address")
        pwd = st.text_input("Enter a password", type="password")
        f_name = st.text_input("First Name")
        l_name = st.text_input("Last Name")
        age = st.text_input("Age ")
        gender = st.radio("Gender",('Male','Female','Other','Prefer not to say'))
        skills = st.multiselect('Skills',['Java', 'R', 'Python', 'C', 'C#', 'React', 'C++', 'Hadoop', 'Ruby', 'Kotlin','Go'])
        experience = st.radio('Experience',('Yes','No'))
        if experience == 'Yes':
            exp = st.text_area("Enter your experience")
        sear = st.text_input("Dream Role")
        location = st.text_input("Location")
        company = st.text_input("Dream Company")
        submission = st.form_submit_button(label="Sign Up")
        if submission == True:
            data = [email, pwd, f_name, l_name,age, gender, skills, experience, exp, sear,location, company]
            with open('D:/COLLEGE/YEAR V/SEM IX/MINOR PROJECT/proj/users.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                f.close()
            st.success("Hello {}, You are successfully registered in rise.com".format(f_name))
            st_lottie(lottie_success, height=100, key="animation")



with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        form()
    with right_column:
        st.write("##")
        st.write("##")
        st_lottie(lottie_coding, height=1000, key="anime")