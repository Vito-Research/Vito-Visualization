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
        st.subheader("Heartrate")
        link = '[Stanford Code](https://github.com/StanfordBioinformatics/wearable-infection)'
        st.markdown(link, unsafe_allow_html=True)

        link = '[Stanford General Info](https://med.stanford.edu/news/all-news/2020/12/smartwatch-can-detect-early-signs-of-illness.html)'
        st.markdown(link, unsafe_allow_html=True)

        link = '[Stanford Data](https://us10.campaign-archive.com/?u=7009b0b0171f7f3d47cfa11d1&id=327f4f582f)'
        st.markdown(link, unsafe_allow_html=True)

        link = '[Stanford Research Paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8240687/)'
        st.markdown(link, unsafe_allow_html=True)

        st.subheader("Respiratory Rate")
        link = '[Respiratory Rate Info](https://www.healio.com/news/primary-care/20210527/oxygen-saturation-respiratory-rate-predict-covid19-mortality)'
        st.markdown(link, unsafe_allow_html=True)

        link = '[Respiratory Rate Study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0243693)'
        st.markdown(link, unsafe_allow_html=True)

        st.subheader("Blood Oxygen")
        link = '[UW Study](https://newsroom.uw.edu/news/covid-19-mortality-linked-signs-easily-measured-home)'
        st.markdown(link, unsafe_allow_html=True)

        
    with st.expander("Risk Documentation (Heartrate)"):
    
        st.write("1) Get active energy when its below or equal to 1  (indicates you are asleep) ")
            

        st.write("2) Get average heartrate from the start date of the active energy below and end date")
            

        st.write("3) Filter the averages into days")
           

        st.write("4) Get average for each day (expect for the last/current) day store in an array")
           
        
        st.write("5) If the median + 3 is less than average for last night/current day then the day is categorized as red")
          

        st.write("6) If two consecutive days are in red, then an alert is sent")
    with st.expander("Github Links"):
        col1, col2, col3 = st.columns(3)
        link = '[Visualization App](https://github.com/AndreasInk/Vito-Visualization)'
        link2 = '[New iOS App](https://github.com/AndreasInk/Vito)'
        link3 = '[Old iOS App](https://github.com/AndreasInk/Rhythm)'
        col1.markdown(link, unsafe_allow_html=True)
        col2.markdown(link2, unsafe_allow_html=True)
        col3.markdown(link3, unsafe_allow_html=True)
           

