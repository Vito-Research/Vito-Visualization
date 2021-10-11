
from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import  nightsignal as ns
import json
import csv
import datetime
import os
from playsound import playsound
import numpy as np
def analyze():
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
        
        col1, col2, col3 = st.columns(3)

        # col1.table(df)
        # col3.table(df2)
        ns.getScore("/tmp/tmp.csv", "/tmp/tmp2.csv")

        

        
        f = open('/tmp/NS-signals.json',)
    
    # returns JSON object as
    # a dictionary
        data = json.load(f)
        
        #st.write(data)
        alerts = data['nightsignal']
        if RiskFile is not None:
            alertVals = []
            allAlertVals = []
            allDates = []
            for item in alerts:
                #st.write(item["val"])
                allAlertVals.append(item["val"])
                
                allDates.append(item["date"])
                if int(item["val"]) > 0:
                    
                    alertVals.append(item["val"])
        
            nsAlertCount = len(alertVals)
            df2 = pd.read_csv(RiskFile)
            vitoAlertCount = len(df2[df2['Risk'] == 1])
            
            # st.write(nsAlertCount)
            # st.write(vitoAlertCount)
            col1, col2 = st.columns(2)
            col1.subheader("Vito Alerts: " + str(vitoAlertCount)) 
            col2.subheader("NightSignal Alerts: " + str(nsAlertCount)) 
            if nsAlertCount == vitoAlertCount:
                st.balloons()
                st.success("ALGORITHMS MATCH!!!!!!!!")
                #playsound("success.mp4")
            else:
                st.error("No Match")

        col1, col2 = st.columns(2)

        df = DataFrame()
        df.insert(0, "Start_Date_Risk", allDates, True)
        df.insert(0, "NS Alerts", allAlertVals, True)

        
        #col1.bar_chart(df.set_index('Value'))
        
        # st.table(df)
        # st.table(df2)
        i = 0
       
        
        df2["Risk"] = df2["Risk"].astype(int)
        df["NS Alerts"] = df["NS Alerts"].astype(int)
        df["Start_Date_Risk"] = pd.to_datetime(df["Start_Date_Risk"])
        df2["Start_Date_Risk"] = pd.to_datetime(df2["Start_Date_Risk"])
        df_merged = pd.merge(df, df2, how='outer', on ="Start_Date_Risk") 
        #df_merged = pd.merge(df, df2, right_on= "Start_Date_Risk", left_on="Start_Date_Risk")
        df_merged = df_merged.drop('Start_Time_Risk', 1)
       
       
        df_merged = df_merged[ ['Risk'] + [ col for col in df_merged.columns if col != 'Risk' ] ]
        #st.table(df_merged)
        
        count = df_merged.shape[0]
        devices = []
        incorrect = []
        for i in range(count):
            row = df_merged.iloc[i]
           
            if row["Risk"] != row["NS Alerts"]:
                incorrect.append(row)

        heartratedf = pd.read_csv("/tmp/tmp.csv")
        
        #heartratedf["Start_Date_Risk"] = pd.to_datetime(heartratedf["Start_Date"])
        incorrect = pd.DataFrame(incorrect)
        
        count = heartratedf.shape[0]
        devices = []
        
        
        for i in range(count):
            row = heartratedf.iloc[i]
            start = datetime.datetime.strptime( row.Start_Date, '%Y-%m-%d' )
            row.Start_Date = start
        heartratedf["Start_Date_Risk"] = pd.to_datetime(heartratedf["Start_Date"])
        
        heartratedf = heartratedf.groupby ('Start_Date_Risk' )["Heartrate"].median()
        #st.table(incorrect)
        incorrect = pd.merge(incorrect, heartratedf, how='outer', on ="Start_Date_Risk") 
        # incorrect = incorrect.drop('Start_Date', 1)
        # incorrect = incorrect.drop("Start_Time", 1)
        st.header("Conflicting Alerts")      
        st.table(incorrect)
        with st.expander("See full data"):
            
            #df_merged = df.append(df2)
            st.table(df_merged)
        #st.header("Conflicting Scores")
        col1, col2 = st.columns(2)

        df = DataFrame()
        df.insert(0, "Start_Date_Risk", allDates, True)
        df.insert(0, "Value", allAlertVals, True)
    
        # col1.table(df2)
        # col2.table(alerts)


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