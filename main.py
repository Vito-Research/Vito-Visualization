
import streamlit as st
import pandas as pd
import  nightsignal as ns
import json
import csv
import datetime
HRFile = st.file_uploader("Upload Heartrate Data", type=("csv"))

StepFile = st.file_uploader("Upload Step Data", type=("csv"))


RiskFile = st.file_uploader("Upload Risk Data", type=("csv"))


if HRFile is not None:
    df = pd.read_csv(HRFile)
    df.to_csv("tmp.csv")

    df2 = pd.read_csv("Steps.csv")
    
    #df2['Steps'] = []
    count = df.shape[0]
    
    i = 0
    # while i < count:
    #     row = df.iloc[i]
    #     df2['Steps'] += 0
    #     start = datetime.datetime.strptime( row.Start_Time, '%H:%M:%S' )
    #     start - datetime.timedelta(minutes=5)
    #     endTime = start + datetime.timedelta(minutes=5)
                    
    #     end = datetime.datetime.strptime(endTime.strftime("%H:%M:%S"), '%H:%M:%S' )
    #     df2['Start_Date'] += row
        
    #     df2['End_Date'] += row.Start_Date

    #     df2['End_Time'] += endTime.strftime("%H:%M:%S")
    #     df2.to_csv("StepFile.csv")
    #     i += 1
    ns.getScore("tmp.csv", "Steps.csv")

    


    f = open('NS-signals.json',)
 
# returns JSON object as
# a dictionary
    data = json.load(f)
      
    #st.write(data)
    alerts = data['nightsignal']
    if RiskFile is not None:
        nsAlertCount = len(alerts)
        df = pd.read_csv(RiskFile)
        vitoAlertCount = len(df[df['Risk'] == 1])
        st.write(nsAlertCount)
        st.write(vitoAlertCount)


