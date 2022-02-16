from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import  nightsignal as ns
import json
import datetime
import os
import time
def add_blank_rows(df, no_rows):
    df_new = pd.DataFrame(columns=df.columns)
    for idx in range(len(df)):
        df_new = df_new.append(df.iloc[idx])
        for _ in range(no_rows):
            df_new=df_new.append(pd.Series(), ignore_index=True)
    return df_new
def analyze():
    st.header("Add Your File")

    HRFile = st.file_uploader("Upload Heartrate Data", type=("csv"))

    #StepFile = st.file_uploader("Upload Step Data", type=("csv"))

    HRFileName = ""
    RiskFileName = ""
   # RiskFile = st.file_uploader("Upload Risk Data", type=("csv"))

    def processData(HRFile):
        df = pd.DataFrame()
        df = pd.read_csv(HRFile)
        df.to_csv(os.path.join("/tmp/tmp.csv"))
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
            endTime = start  + datetime.timedelta(minutes=30)
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
        df2.to_csv(os.path.join("/tmp/tmp2.csv"))
        
        col1, col2, col3 = st.columns(3)

        # col1.table(df)
        # col3.table(df2)
        ns.getScore(os.path.join("/tmp/tmp.csv"), "/tmp/tmp2.csv")

        

        
        f = open(os.path.join('/tmp/NS-signals.json'), "r")
    
    # returns JSON object as
    # a dictionary
        data = json.load(f)
        
        #st.write(data)
        alerts = data['nightsignal']
        if HRFile is not None:
            alertVals = []
            allAlertVals = []
            allDates = []
            for item in alerts:
                #st.write(item["val"])
                allAlertVals.append(item["val"])
                
                allDates.append(item["date"])
                if int(item["val"]) > 1:
                    
                    alertVals.append(item["val"])
        
            nsAlertCount = len(alertVals)
            #st.write(alertVals)
            # df2 = pd.read_csv(HRFile)
            # df2 = df2.drop_duplicates()
            vitoAlertCount = len(df[df['Risk'] > 0.9])
            
            # st.write(nsAlertCount)
            # st.write(vitoAlertCount)
           
            

        col1, col2 = st.columns(2)
        newDates = []
        newAlerts = []
        df2 = DataFrame()
        for i in range(len(allDates)):
                #st.write(allDates[i][:7])
                targetDates = []
                for date in df["Start_Date"]:
                    targetDates.append(date[:7])
                #st.write(df["Start_Date"][:7])
                if allDates[i][:7] in targetDates:
                    newDates.append(allDates[i])
                    newAlerts.append(allAlertVals[i])
           
               
        df2.insert(0, "Start_Date_Risk", newDates, True)
        df2.insert(0, "NS Alerts", newAlerts, True)
        #df = df.remove_duplicates()
        
        #col1.bar_chart(df.set_index('Value'))
        
        # st.table(df)
        # st.table(df2)
        # count = df.shape[0]
        # count = df.shape[0]
        i = 0
        # for i in range(2): 
        #     row = df2.iloc[1] 
            
            #df2 = df2.append(row, ignore_index=True)
        df2["NS Alerts"] = df2["NS Alerts"].replace(to_replace ="1",
                 value ="0")
        df2["NS Alerts"] = df2["NS Alerts"].replace(to_replace ="2",
                 value ="1")
       
        df["Risk"] = df["Risk"].astype(int)
        df2["NS Alerts"] = df2["NS Alerts"].astype(int)
        # st.table(df2)
        # st.table(df)
        df2.rename(columns={"NS Alerts": "Risk"}, inplace=True)
        df2.rename(columns={"Start_Date_Risk": "Start_Date"}, inplace=True)
        #df2.rename(columns={'Start_Date_Risk': 'Start_Date'}, inplace=True)
        # st.table(df2)
        df["Start_Date"] = pd.to_datetime(df["Start_Date"])
        df2["Start_Date"] = pd.to_datetime(df2["Start_Date"])
        # df2["Start_Date_Risk"] = pd.to_datetime(df2["Start_Date_Risk"])
        df_merged = pd.merge(df, df2, how='outer', on ="Start_Date")
        df_merged = df_merged.dropna() 
        #df_merged = pd.merge(df, df2, right_on= "Start_Date", left_on="Start_Date")
       # df_merged = df_merged.drop('Start_Time_Risk', 1)
       
       
        #df_merged = df_merged[ ['Risk'] + [ col for col in df_merged.columns if col != 'Risk' ] ]
        
        #df_merged = pd.concat([df,df2], join='inner', axis=1)
        #df_merged = pd.concat([df.set_index('Start_Date'), df2.set_index('Start_Date')], 
                #   axis='columns', keys=['First', 'Second'], join="outer" )
        # df_merged.swaplevel(axis='columns')[df_merged.columns[1:]]
        df = df.drop('Heartrate', 1)
        df = df.drop('Start_Time', 1)
        df = df.drop('Device', 1)
        column_names = ["Risk", "Start_Date"]

        #df = df.reindex(columns=column_names)
        # df = df.fillna(df2['Start_Date'])
        # df2 = df2.fillna(df['Start_Date'])
        count = (df2.shape[0] - df.shape[0])
        vitoCount = df_merged[df_merged["Risk_y"] == 1].shape[0]
        nsCount = df_merged[df_merged["Risk_x"] == 1].shape[0]
        col1, col2 = st.columns(2)
        col1.subheader("Vito Alerts: " + str(vitoCount)) 
        col2.subheader("NightSignal Alerts: " + str(nsCount)) 
        if nsAlertCount == vitoAlertCount:
            st.balloons()
            st.success("ALGORITHMS MATCH!!!!!!!!")
            #playsound("success.mp4")
        else:
            st.write("")
        #df = add_blank_rows(df, count)
        df["Start_Date"] = pd.to_datetime(df["Start_Date"])
        df2["Start_Date"] = pd.to_datetime(df2["Start_Date"])
        # st.table(df)
        # st.table(df2)
        # for i in range(df2.shape[0]):
        #     if df2.Start_Date[i] not in df.Start_Date:

        #         df1 = pd.DataFrame([[np.nan] * len(df.columns)], columns=df.columns)
        #         df.loc[i] = df1.loc[0]
        # ne = (df1 != df2).any(1)
        df.append(df2)
        
 
        # df_merge = df.groupby("Start_Date")
        # df_merged = pd.DataFrame().append(df_merge.first())
        # df_merged.append(df_merge.last())
        # st.table(df_merged)
        #st.write(df_merged["Start_Date"].unique())
        count = df.shape[0]
        devices = []
        incorrect = []
        # for i in range(len(df_merged)):
        #     row = df_merged.iloc[i]
           
        #     if row["Risk"] != row["NS Alerts"]:
        #         if i > 2 and i < count - 1 :
        #             # rowBefore = df.iloc[i - 1]
        #             # rowAfter = df.iloc[i + 1]
        #             # if rowBefore["Start_Date_Risk"] + timedelta(days=1) == row["Start_Date_Risk"] and rowAfter["Start_Date_Risk"] + timedelta(days=-1) == row["Start_Date_Risk"]:
        #             #     if rowBefore["Risk"] != row["NS Alerts"] and rowAfter["Risk"] != row["NS Alerts"]:
                        
        #             incorrect.append(row)
        #             # else:
        #             #      incorrect.append(row)

        heartratedf = pd.read_csv(os.path.join("/tmp/tmp.csv"))
        
        #heartratedf["Start_Date_Risk"] = pd.to_datetime(heartratedf["Start_Date"])
        incorrect = pd.DataFrame(incorrect)
        incorrect = incorrect.rename({"Risk": "Vito Alert"})
        count = heartratedf.shape[0]
        devices = []
        
        
        for i in range(count):
            row = heartratedf.iloc[i]
            start = datetime.datetime.strptime( row.Start_Date, '%Y-%m-%d' )
            row.Start_Date = start
        heartratedf["Start_Date_Risk"] = pd.to_datetime(heartratedf["Start_Date"])
        
        heartratedf = heartratedf.groupby ('Start_Date_Risk' )["Heartrate"].median()
        #st.table(incorrect)
        #incorrect = pd.merge(incorrect, heartratedf, how='outer', on ="Start_Date_Risk") 
        # incorrect = incorrect.drop('Start_Date', 1)
        # incorrect = incorrect.drop("Start_Time", 1)
        incorrect = incorrect.dropna()
        # total = df.shape[0]
        # total_incorrect = incorrect.shape[0]
        #similarity = 1 - total_incorrect/total
        #st.metric("Model Similarity", f"{round(similarity, 3)} %")
        # col1, col2 = st.columns(2)
        # col1.header("NightSignal") 
        # col2.header("Vito") 
        col1, col2 = st.columns(2)
        # col1.table(df)
        # col2.table(df2) 
        st.table(df_merged)
        df_merged.to_csv("/tmp/Vito_Alert_Statistics.csv")
        #st.table(incorrect)
        st.download_button(
            "Download Alert Statistics",
            df_merged.to_csv(line_terminator="\r\n", index=False),
            file_name=os.path.join("NightSignalResult" +'.pdf'),
            on_click=st.balloons,
        )
        with st.expander("See full data"):
            #st.bar_chart(df_merged)
            #df_merged = df.append(df2)
            st.table(df_merged)
        #st.header("Conflicting Scores")
        col1, col2 = st.columns(2)

        df = DataFrame()
        df.insert(0, "Start_Date_Risk", allDates, True)
        df.insert(0, "Value", allAlertVals, True)
    
        # col1.table(df2)
        # col2.table(alerts)


    def file_selector(folder_path='./sample_data/', type="Health"):
        folder_path = folder_path + type
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
        #RiskFileName = file_selector(type="Risk")
        #st.write('HR File `%s`' % HRFileName)
        if HRFileName:
            processData(HRFileName)
            

        
        #st.write('Risk File `%s`' % RiskFileName)
        



        


                

    if HRFile:
        processData(HRFile)

    