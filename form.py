import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Registration", page_icon=":office:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


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
        pwd = st.text_input("Enter a password")
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
        submission = st.form_submit_button(label="Submit")
        if submission == True:
            st.success("Successfully submitted")
            st_lottie(lottie_success, height=100, key="animation")


with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        form()
    with right_column:
        st.write("##")
        st.write("##")
        st_lottie(lottie_coding, height=600, key="anime")