import streamlit as st
from pages.about import about
from pages.analyze import analyze
from pages.compare import compare


def about_page():
    st.markdown("# About")
    st.sidebar.markdown("# About")


def analyze_page():
    st.markdown("# Analyze")
    st.sidebar.markdown("# Analyze")


def compare_page():
    st.markdown("# Compare")
    st.sidebar.markdown("# Compare")


# dict with key representing page selection text and function to call upon
# selection
page_name_to_fxn_mapping = {
    "About": about,
    "Analyze": analyze,
    "Compare": compare,
}

# title, header, caption content
# st.image("./Vito.png")
st.title("Vito")
st.subheader("Detecting Infection With Wearables")
st.caption(
    """
                Learning more about health while maintaining privacy is vital.  Vito empowers you to explore your health and possibly detect infection via your vitals and on-device machine 
                learning.

                """
)

# page selection
selected_page = st.sidebar.selectbox("Select a page", page_name_to_fxn_mapping.keys())
page_name_to_fxn_mapping[selected_page]()
