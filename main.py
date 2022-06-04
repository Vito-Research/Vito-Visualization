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


if __name__ == "__main__":
    landing_page()
