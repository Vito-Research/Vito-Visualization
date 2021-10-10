
import streamlit as st
from analyze import analyze
from about import about
from compare import compare
from API import API
if 'count' not in st.session_state:
	st.session_state.count = 0
if 'count2' not in st.session_state:
	st.session_state.count2 = 0
if 'count3' not in st.session_state:
	st.session_state.count3 = 0
API()
st.image("Vito.png")
st.title("Detecting Infectious Diseases With Wearables")
st.subheader("")
col1, col2 = st.columns(2)
start = col1.button("Anaylze")
learnMore = col2.button("Learn More")
if start:
    st.session_state.count += 1
if st.session_state.count > 0:
        analyze()

if learnMore:
    st.session_state.count2 += 1

if  st.session_state.count2 > 0:
        about()

if compare:
    st.session_state.count3 += 1

if  st.session_state.count3 > 0:
        compare()

