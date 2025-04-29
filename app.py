import requests
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import webbrowser
def URL(match_no, home1, home2, away1, away2, loc, date):
    url = f"https://www.district.in/event/tata-ipl-2025-match-{match_no}-{home1}-{home2}-vs-{away1}-{away2}-in-{loc}-{date}"
    return url

if 'running' not in st.session_state:
    st.session_state.running = False

# Streamlit UI
st.title('IPL Match Ticket Booking')
st.write('Enter the match details and click the button below to start or stop the checking process.')

teams1=["mumbai","lucknow","chennai","punjab","delhi","royal","sunrisers","gujarat","rajasthan","kolkata"]
teams2=["indians","super-giants","super-kings","kings","capitals","challengers-bangalore","hyderabad","titans","royals","night-riders"]
CHECK_INTERVAL = 0.1
TARGET_TEXT = "Sorry! No slots/tickets are currently available to book for TATA IPL 2025 - Match 61 - Punjab Kings vs Mumbai Indians"

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

def check_url(match_no, home1, home2, away1, away2, loc, date):
    url = URL(match_no, home1.lower(), home2.lower(), away1.lower(), away2.lower(), loc.lower(), date.lower()) + "/buy-page"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service() 
    driver = webdriver.Chrome(service=service, options=chrome_options)

    while True:
        try:
            driver.get(url)
            elements = driver.find_elements("class name", "css-1b73o3a")
            if len(elements) > 1 and TARGET_TEXT in elements[1].text:
                st.warning("❌ URL is Active, Tickets not available. Retrying...")
            else:
                st.success("🎉 Tickets available! Opening page...")
                st.markdown(f"""
                    <meta http-equiv="refresh" content="0; url={url}">
                    <p>Redirecting to <a href="{url}">Buy Page</a>...</p>
                """, unsafe_allow_html=True)
                break
        except NoSuchElementException:
            st.error("⚠️ Tickets not available. Retrying...")
        time.sleep(CHECK_INTERVAL)
    driver.quit()


start_button = st.button("Start Checking")
stop_button = st.button("Stop Checking")

if start_button and not st.session_state.running:
    st.session_state.running = True
    st.write("Checking started...")
    check_url(match_no, home1, home2, away1, away2, loc, date)

if stop_button and st.session_state.running:
    st.session_state.running = False
    st.write("Checking stopped.")

