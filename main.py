
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

st.image("Vito.png")
st.title("Vito")
st.subheader("Detecting Infectious Diseases With Wearables")
col1, col2, col3 = st.columns(3)
start = col1.button("Anaylze")
# compareBtn = col2.button("Compare")
learnMore = col2.button("Learn More")

if start:
    st.session_state.count += 1
if st.session_state.count > 0:
        analyze()

if learnMore:
    st.session_state.count2 += 1

if  st.session_state.count2 > 0:
        about()

# if compareBtn:
#     st.session_state.count3 += 1

# if  st.session_state.count3 > 0:
#         compare()

