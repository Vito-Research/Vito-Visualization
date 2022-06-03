
import streamlit as st
import pandas as pd 
import numpy as np 
import datetime
import random
import json
from random import seed
from random import randint
from dataclasses import make_dataclass
import requests
import nightsignal as ns
import os
from sklearn.metrics import accuracy_score

def compare():
    def Convert(lst):
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return res_dct
    seed(1)
    st.title('Random test values')



    today = datetime.date.today()
    symptom1 = today + datetime.timedelta(days=5)
    symptom2 = today + datetime.timedelta(days=10)
    tomorrow = today + datetime.timedelta(days=30)
    start_date = st.date_input('Start date', today)
    symptom_dateStart = st.date_input('symptom date', symptom1)
    symptom_dateFinish = st.date_input('symptom date Finish', symptom2)
    end_date = st.date_input('End date', tomorrow)
    run = st.button("run")
    if run:
        if start_date < end_date:
            st.success('Start date: `%s`\n\nSymptom date start: `%s`\n\nSymptom date Finish: `%s`\n\nEnd date:`%s`' % (start_date,symptom_dateStart,symptom_dateFinish, end_date))
            days_betweenstarttoend=end_date-start_date
            days_betweenstarttofirst=symptom_dateStart-start_date
            days_betweenstarttolast=symptom_dateFinish-start_date
        else:
            st.error('Error: End date must fall after start date.')
        rows, cols = (days_betweenstarttoend.days+2, 1)
        #Date=[]
   
        for i in range(rows):
            col=[]
            for j in range(cols):
                Da=today + datetime.timedelta(days=i-1)
                date_strf=Da.strftime("%Y-%m-%d")
            # Date.append(date_strf)
                if i==0:
                #df=pd.DataFrame([[1, 2]],columns=list('DB'),index=['x'])
                
                    df=pd.DataFrame([[date_strf,"02:08:15", randint(60,61), 0]],columns=["Start_Date", "Start_Time", "Heartrate", "Risk"],index=['x'])

                    continue
                #    
                if  i<=days_betweenstarttolast.days and i>=days_betweenstarttofirst.days:
                    df2= pd.DataFrame([[date_strf, "02:08:15", randint(95,100), 0]],columns=["Start_Date", "Start_Time", "Heartrate", "Risk"],index=['x']) 
                    df=df.append(df2)
                
                # col.append(randint(65,66))
                # Date.append(col) 
                    continue
                if i<=days_betweenstarttofirst.days or i>=days_betweenstarttolast.days: 
                    df3= pd.DataFrame([[date_strf, "02:08:15", randint(60,61), 0]],columns=["Start_Date", "Start_Time", "Heartrate", "Risk"],index=['x']) 
                # df=df.append(df3)
                    df= df.append(df3)
                # st.write(df)
                # col.append(randint(60,61))
                # Date.append(col)    
        st.write(df)
        # csv = 'report.csv'
        # df.to_csv(csv)

        url = "https://testingcer.herokuapp.com/"
        jsonData = {}
        jsonData["arr"] = df["Heartrate"].tolist()
        st.text(json.dumps(jsonData))
        r = requests.post(url, json= jsonData)
    
        st.write(r.text)
    
        df.to_csv(os.path.join("tmp.csv"))
        count = df.shape[0]
        devices = []
        for i in range(count):
            devices.append("HK Apple Watch")
        df.insert(0, "Device", devices, True)

        dfSteps = pd.DataFrame()
        i = 0
        steps = []
        start_time = []
        end_time = []
        end_date = []
        start_date = []

        dfSteps.insert(0, "Steps", steps, True)
        dfSteps.insert(0, "Start_Date", start_date, True)
        dfSteps.insert(0, "Start_Time", start_time, True)
        dfSteps.insert(0, "End_Date", start_date, True)
        dfSteps.insert(0, "End_Time", end_time, True)
        dfSteps.to_csv(os.path.join("/tmp/tmp2.csv"))

        ns.getScore(os.path.join("/tmp/tmp.csv"), "/tmp/tmp2.csv")
        
        with open(os.path.join('/tmp/NS-signals.json'), "r") as f:

                data = json.load(f)
                os.system("rm " + os.path.join("/tmp/NS-signals.json"))
                os.system("rm " + os.path.join("/tmp/tmp.csv"))
                vitoArr = [int(s) for s in r.text.split(",") if s.isdigit()]
                alerts = data['nightsignal']
                allAlertVals = []
                allDates = []
                for item in alerts:

                    allAlertVals.append(item["val"])
                st.write(vitoArr)
                st.sidebar.header(
            "Accuracy: " + str(accuracy_score(allAlertVals, vitoArr)))
       

compare()