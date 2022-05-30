
import streamlit as st

from about import about
from analyze import analyze
from compare import compare
##########################################
if 'learnMore' not in st.session_state:
    st.session_state.learnMore = True

if 'compare' not in st.session_state:
    st.session_state.compare = False
    
if 'count2' not in st.session_state:
    st.session_state.count2 = 0


    
if 'count3' not in st.session_state:
    st.session_state.count3 = 0
###########################################

    


###############################################################
st.image("./Vito.png")
st.title("Vito")
st.subheader("Detecting Infection With Wearables")
###############################################################


##############################################################################################################
st.caption(
                """
                Learning more about health while maintaining privacy is vital.  Vito empowers you to explore your health and possibly detect infection via your vitals and on-device machine 
                learning.

                """
           )
##############################################################################################################



##################################               
col1, col2, col3 = st.columns(3)

start = col1.button("Analyze")
st.session_state.compare = col2.button("Compare")
##################################


##################################################
if start:
    st.session_state.learnMore = False

st.session_state.learnMore = col3.button("About")

if st.session_state.learnMore:
    about()

else:
    if st.session_state.compare:
        compare()
    else:
        analyze()
##################################################
