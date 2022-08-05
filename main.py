import streamlit as st

# TODO: hard to tell what the diff between analysis and analyze are


def landing_page():
    # title, header, caption content
    st.image("./Vito.png")
    st.title("Vito")
    st.subheader("Detecting Infection With Wearables")
    st.caption(
        """
                    Learning more about health while maintaining privacy is vital.  Vito empowers you to explore your health and possibly detect infection via your vitals and on-device machine 
                    learning.
    
                    """
    )
    st.image("./Overview.png")
    st.markdown(
        "- This web app is designed to illustrate how Vito works\n"
        "- We are a group of students developing open-source tools to fight pandemics\n"
        "- If you'd like to contribute... [click here](https://github.com/Vito-Research/Vito-Visualization)"
    )


if __name__ == "__main__":
    landing_page()
