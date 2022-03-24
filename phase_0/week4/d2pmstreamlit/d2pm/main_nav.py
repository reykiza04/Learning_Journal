import data_vis,hypo_tes
import streamlit as st
PAGES ={
    'Data Visualization': data_vis,
    'Hypoteshis testing' : hypo_tes
}

selected = st.sidebar.selectbox('select a page',list(PAGES.keys()))

page = PAGES[selected]

page.app() #biar ga ribet fungsinya samakan saja agar pemanggilanya metodenya