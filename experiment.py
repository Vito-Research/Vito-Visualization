from pandas.core.frame import DataFrame
import streamlit as st
import createRandom as cr
import nightsignal as ns
import analyze as an
import time




min = st.number_input('Enter Min')
max = st.number_input('Enter Max')
steps = st.number_input('Enter Steps')
countOfData = st.number_input('# of Datapoints')
run = st.button("Run")
if run:
   
    DataFrame().to_csv("/tmp/NS-signals.json")
    cr.createRandomData(int(min), int(max), int(steps), int(countOfData))

    an.processData("random.csv", "sample_data/Risk/Vito_Risk_Data_A.csv")

