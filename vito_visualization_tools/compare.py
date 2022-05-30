
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
def compare():
    seed(1)
    st.title('Random test values')



    today = datetime.date.today()
    symptom1 = today + datetime.timedelta(days=1)
    symptom2= today + datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    start_date = st.date_input('Start date', today)
    symptom_dateStart = st.date_input('symptom date', symptom1)
    symptom_dateFinish = st.date_input('symptom date Finish', symptom2)
    end_date = st.date_input('End date', tomorrow)
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
            date_strf=Da.strftime("%m/%d/%Y")
        # Date.append(date_strf)
            if i==0:
            #df=pd.DataFrame([[1, 2]],columns=list('DB'),index=['x'])
            
                df=pd.DataFrame([[date_strf,randint(60,61)]],columns=list('DB'),index=['x'])

                continue
            #    
            if  i<=days_betweenstarttolast.days and i>=days_betweenstarttofirst.days:
                df2= pd.DataFrame([[date_strf,randint(65,66)]],columns=list('DB'),index=['x']) 
                df=df.append(df2)
            
            # col.append(randint(65,66))
            # Date.append(col) 
                continue
            if i<=days_betweenstarttofirst.days or i>=days_betweenstarttolast.days: 
                df3= pd.DataFrame([[date_strf,randint(60,61)]],columns=list('DB'),index=['x']) 
            # df=df.append(df3)
                df= df.append(df3)
            # st.write(df)
            # col.append(randint(60,61))
            # Date.append(col)    
    st.write(df)
    # csv = 'report.csv'
    # df.to_csv(csv)
    # url = "http://127.0.0.1:8081"

    # r = requests.post(url, json= json.dumps(df.values.tolist()))
    # st.write(r)