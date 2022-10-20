import streamlit as st
import requests
from streamlit_lottie import st_lottie
#import form.py


st.set_page_config(page_title="Rise - Home Page", page_icon=":office:", layout="wide")



def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")
#LOAD ASSETS
lottie_coding = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_3jmvq04g.json")
#lottie_reg = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_pprxh53t.json")
#lottie_success = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_t58qlnnx.json")

#HEADER
with st.container():
    st.subheader("Hi! Welcome! :wave:" )
    st.title("rise.com - The perfect site for your perfect job")
    st.subheader("**R**eveal your **I**nner **S**trengths to **E**mployers")
    st.write("This site will help you find the most suitable job by aggregating from various job portals and improve your skillset as well")
    st.write("[Register here >](https://www.naukri.com/mnjuser/homepage)")

#WHAT WE DO
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What we do")
        st.write("##")
        st.write(
            """
                        In day to day life, there are many opportunities that are available and the number of
            startups are also growing and emerging in the technical industry. Being a fresher, it&#39;s quite a
            difficult task to keep track of all the opportunities that are available in the market and it is
            increasingly troublesome to keep track of every job opening. There are also chances that
            we might miss the opportunity without knowing about it. The main objective of this project is
            to accumulate all the available opportunities in a specific domain and the boundary/location
            can also be specified if there are any boundary restrictions or constraints. After accumulating
            the opportunities, an analysis will be done to predict the skills and roles that are in demand.
            With this project, we can explore many opportunities and we can go for the ones that we are
            really interested in and ace it. The ultimate aim is to aggregate and recommend appropriate
            jobs to job seekers.
            """
        )
        #st.write("h")
    with right_column:
        st_lottie(lottie_coding, height=400, key="anime")

#CONTACT

with st.container():
    st.write("---")
    st.header("Get in Touch with us!")
    st.write("##")

    contact_form = """
    <form action="https://formsubmit.co/desidecor20@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder = "Your name" required>
        <input type="email" name="email" placeholder = "Your email" required>
        <textarea name = "message" placeholder = "Your message.." required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()

