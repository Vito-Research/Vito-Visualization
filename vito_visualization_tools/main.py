
import streamlit as st

from about import about
from analyze import analyze

##########################################
if 'learnMore' not in st.session_state:
    st.session_state.learnMore = True


    
if 'count2' not in st.session_state:
    st.session_state.count2 = 0


    
if 'count3' not in st.session_state:
    st.session_state.count3 = 0
###########################################

    


###############################################################
st.image("../Vito.png")
st.title("Vito")
st.subheader("Detecting Infectious Diseases With Wearables")
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
##################################


##################################################
if start:
    st.session_state.learnMore = False

st.session_state.learnMore = col2.button("About")

if st.session_state.learnMore:
    about()

else:
    analyze()
##################################################
