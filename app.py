
import streamlit as st

# Importing pages
import hyper_roll


PAGES = {
    "Hyper roll": hyper_roll,
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.main()

