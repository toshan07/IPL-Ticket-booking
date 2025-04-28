import requests
import time
import webbrowser
import streamlit as st

def URL(match_no, home1, home2, away1, away2, loc, date):
    url = f"https://www.district.in/event/tata-ipl-2025-match-{match_no}-{home1}-{home2}-vs-{away1}-{away2}-in-{loc}-{date}"
    return url

if 'running' not in st.session_state:
    st.session_state.running = False

# Streamlit UI
st.title('IPL Match URL Checker')
st.write('Click the button below to start or stop the checking process.')

teams1=["mumbai","lucknow","chennai","punjab","delhi","royal","sunrisers","gujarat","rajasthan","kolkata"]
teams2=["indians","super-giants","super-kings","kings","capitals","challengers-bangalore","hyderabad","titans","royals","night-riders"]

with st.form(key='match_form'):
    match_no=st.text_input('Match Number', '61')  
    home1 = st.selectbox('Home Team 1',teams1,index=0)
    home2 = st.selectbox('Home Team 2',teams2,index=0)
    away1 = st.selectbox('Away Team 1',teams1,index=0)
    away2 = st.selectbox('Away Team 2',teams2,index=0)
    loc = st.text_input('Location','dharamsala')
    date = st.text_input('Date','may11')
    submit_button = st.form_submit_button(label='Generate URL')


if submit_button:
    url = URL(match_no, home1, home2, away1, away2, loc, date)
    st.write(f"Generated URL: [Click here]({url})")

start_button = st.button("Start Checking")
stop_button = st.button("Stop Checking")

def check_url(match_no, home1, home2, away1, away2, loc, date):
    url = URL(match_no, home1.lower(), home2.lower(), away1.lower(), away2.lower(), loc.lower(), date.lower())
    c = -1
    while st.session_state.running:
        try:
            response = requests.get(url)
            if response.status_code != 404:
                st.success(f"✅ URL is now accessible! Status: {response.status_code}")
                url += "/buy-page"
                webbrowser.open(url)  
                break
            else:
                c += 1
                if c % 10 == 0:
                    st.warning("❌ Not found. Retrying...")
        except requests.RequestException as e:
            st.error(f"⚠ Error occurred: {e}")
        time.sleep(0.1)

if start_button and not st.session_state.running:
    st.session_state.running = True
    st.write("Checking started...")
    check_url(match_no, home1, home2, away1, away2, loc, date)

if stop_button and st.session_state.running:
    st.session_state.running = False
    st.write("Checking stopped.")
