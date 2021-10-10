
from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import  nightsignal as ns
import json
import csv
import datetime
import os
from playsound import playsound

st.header("Add Your File")

HRFile = st.file_uploader("Upload Heartrate Data", type=("csv"))

#StepFile = st.file_uploader("Upload Step Data", type=("csv"))

HRFileName = ""
RiskFileName = ""
RiskFile = st.file_uploader("Upload Risk Data", type=("csv"))

def processData(HRFile, RiskFile):
    df = pd.read_csv(HRFile)
    df.to_csv("/tmp/tmp.csv")
    count = df.shape[0]
    devices = []
    for i in range(count):
        devices.append("HK Apple Watch")
    df.insert(0, "Device", devices, True)
   
    df2 = DataFrame()
    i = 0
    steps = []
    start_time = []
    end_time = []
    end_date = []
    start_date = []
    for i in range(count):
        
        row = df.iloc[i]
        
        start = datetime.datetime.strptime( row.Start_Time, '%H:%M:%S' )
        endTime = start + datetime.timedelta(minutes=30)
        start = start - datetime.timedelta(minutes=30)
        
                    
        end = datetime.datetime.strptime(endTime.strftime("%H:%M:%S"), '%H:%M:%S' )
        start_time.append(start.strftime("%H:%M:%S"))
        end_time.append(endTime.strftime("%H:%M:%S"))
        steps.append(0)
        start_date.append(row.Start_Date)
        end_date.append(row.Start_Date)

        i += 1
        
    df2.insert(0, "Steps", steps, True)
    df2.insert(0, "Start_Date", start_date, True)
    df2.insert(0, "Start_Time", start_time, True)
    df2.insert(0, "End_Date", start_date, True)
    df2.insert(0, "End_Time", end_time, True)
    df2.to_csv("/tmp/tmp2.csv")
       
    ns.getScore("/tmp/tmp.csv", "/tmp/tmp2.csv")

    

    
    f = open('NS-signals.json',)
 
# returns JSON object as
# a dictionary
    data = json.load(f)
      
    #st.write(data)
    alerts = data['nightsignal']
    if RiskFile is not None:
        alertVals = []
        for item in alerts:
            #st.write(item["val"])
            if int(item["val"]) > 0:
                
                alertVals.append(item["val"])
       
        nsAlertCount = len(alertVals)
        df = pd.read_csv(RiskFile)
        vitoAlertCount = len(df[df['Risk'] == 1])
        # st.write(nsAlertCount)
        # st.write(vitoAlertCount)
        if nsAlertCount == vitoAlertCount:
            st.balloons()
            st.success("ALGORITHMS MATCH!!!!!!!!")
            #playsound("success.mp4")
        else:
            st.error("No Match")
def file_selector(folder_path='.', type="Heartrate"):
    filenames = os.listdir(folder_path)
    csvFiles = []
    for file in filenames:
        if "csv" in file:
            csvFiles.append(file)
    selected_filename = st.selectbox('Select ' + type, csvFiles)
    return os.path.join(folder_path, selected_filename)


if HRFile is None:
    st.header("Or Select A File")
    HRFileName = file_selector(type="Health")
    st.write('HR File `%s`' % HRFileName)
    if RiskFileName:
        processData(HRFileName, RiskFileName)
        
if RiskFile is None:
    RiskFileName = file_selector(type="Risk")
    st.write('Risk File `%s`' % RiskFileName)
    if RiskFileName:
        processData(HRFileName, RiskFileName)


    


            

if HRFile and RiskFile:
    processData(HRFile, RiskFile)