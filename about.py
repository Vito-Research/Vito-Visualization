import streamlit as st

def about():
    
    with st.expander("Why It Matters"):
        st.write("""The lead developer and founder of Vito, Andreas Ink, envisions more access and understanding of health.  

Andreas’s Dad and Aunt's diagnosis of Parkinson’s and a combination of other conditions, resulted in his two relatives having a weakened immune system, leading Andreas to brainstorm solutions to combat the risk of infectious diseases.  

In an effort to reduce transmission of infectious diseases from the university where Andreas studies to home where his immuno-compromised Dad is, Andreas, Mohamed Elbatouty, and Muhib Sheikh created Vito.


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
    
        st.write("1) Get active energy when its below or equal to 1  (indicates you are asleep) ")
            

        st.write("2) Get average heartrate from the start date of the active energy below and end date")
            

        st.write("3) Filter the averages into days")
           

        st.write("4) Get average for each day (expect for the last/current) day store in an array")
           
        
        st.write("5) If the median + 3 is less than average for last night/current day then the day is categorized as red")
          

        st.write("6) If two consecutive days are in red, then an alert is sent")
           

