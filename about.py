import streamlit as st

def about():
    
    with st.expander("Why It Matters"):
        st.write("""The lead developer and founder of Vito, Andreas Ink, envisions more access and understanding of one’s health.  

Andreas’s Dad and Aunt's diagnosis of Parkinson’s and a combination of other conditions, resulted in his two relatives having a weakened immune system, leading Andreas to brainstorm solutions to combat the risk of infectious diseases.  

In an effort to reduce transmission of infectious diseases from the university where Andreas studies to home where his immuno-compromised Dad is, Andreas and a few of his friends created Vito.


Vito is an app that empowers people to make more informed decisions on visiting immunocompromised individuals like Andreas’s Dad and Aunt and venturing to high-risk areas for infectious disease transmission.
""")
        
    with st.expander("How it Works"):
        st.write("""Vito and it's on-device machine learning empowers people with their vitals.  

Our first feature, the ability to possibly detect the onset of infectious diseases before symptom onset is based on a Stanford study that suggests abnormally high resting heart rate (heart rate while asleep) may indicate infectious illness.  

Vito takes it a step further by improving NightSignal, Stanford's model by incorporating new vitals into the machine learning model, respiratory rate and blood oxygen levels into NightSignal.
""")

    # with st.expander("Roadmap"):
    #     st.write("Roadmap")

    with st.expander("Research"):
        st.write("Research")
     

    with st.expander("Code Documentation"):
    
        st.code("In Progress")

