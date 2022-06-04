import json
import os

import pandas as pd
import streamlit as st
from pandas.core.frame import DataFrame
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from . import nightsignal as ns

from .analysis import analysis
def add_blank_rows(df, no_rows):
    df_new = pd.DataFrame(columns=df.columns)
    for idx in range(len(df)):
        df_new = df_new.append(df.iloc[idx])
        for _ in range(no_rows):
            df_new = df_new.append(pd.Series(), ignore_index=True)
    return df_new


def analyze():

    nsTotal = {'nsTotal': 0}
    vitoTotal = {'vitoTotal': 0}
    matchingTotal = {'matchingTotal': 0}
    averages = {'averages': []}
    kappaArr = {'kappa': []}
    precisionArr = {'precision': []}
    recallArr = {'recall': []}

    all = {'all': pd.DataFrame()}

    st.header("Add Your File")

    HRFile = st.file_uploader("Upload Heartrate Data", type=("csv"))

    HRFileName = ""
    RiskFileName = ""

    def processData(HRFile):

        df = pd.DataFrame()
        df = pd.read_csv(HRFile)
        df.to_csv(os.path.join("/tmp/tmp.csv"))
        count = df.shape[0]
        devices = []
        for i in range(count):
            devices.append("HK Apple Watch")
        df.insert(0, "Device", devices, True)

        dfSteps = DataFrame()
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

        col1, col2, col3 = st.columns(3)

        ns.getScore(os.path.join("/tmp/tmp.csv"), "/tmp/tmp2.csv")

        with open(os.path.join('/tmp/NS-signals.json'), "r") as f:

            data = json.load(f)
            os.system("rm " + os.path.join("/tmp/NS-signals.json"))
            os.system("rm " + os.path.join("/tmp/tmp.csv"))

        alerts = data['nightsignal']
        if HRFile is not None:
            alertVals = []
            allAlertVals = []
            allDates = []
            for item in alerts:

                allAlertVals.append(item["val"])

                allDates.append(item["date"])
                if int(item["val"]) > 1:

                    alertVals.append(item["val"])

            nsAlertCount = len(alertVals)

            vitoAlertCount = len(df[df['Risk'] > 0.9])

        col1, col2 = st.columns(2)
        newDates = []
        newAlerts = []
        df2 = DataFrame()
        for i in range(len(allDates)):

            targetDates = []
            for date in df["Start_Date"]:
                targetDates.append(date)

            if allDates[i] in targetDates:
                newDates.append(allDates[i])
                newAlerts.append(allAlertVals[i])

        df2.insert(0, "Start_Date_Risk", newDates, True)
        df2.insert(0, "NS Alerts", newAlerts, True)
        df2["NS Alerts"] = df2["NS Alerts"].replace(to_replace="1",
                                                    value="0")
        df2["NS Alerts"] = df2["NS Alerts"].replace(to_replace="2",
                                                    value="1")

        df["Risk"] = df["Risk"].astype(int)
        df2["NS Alerts"] = df2["NS Alerts"].astype(int)
        df2.rename(columns={"Start_Date_Risk": "Start_Date"}, inplace=True)
        df["Start_Date"] = pd.to_datetime(df["Start_Date"])
        df2["Start_Date"] = pd.to_datetime(df2["Start_Date"])
        df_merged = pd.merge(df, df2, how='inner', on="Start_Date")

        df_merged = df_merged.dropna()
        df = df.drop('Heartrate', 1)
        df = df.drop('Start_Time', 1)
        df = df.drop('Device', 1)
        column_names = ["Risk", "Start_Date"]

        count = (df2.shape[0] - df.shape[0])

        vitoCount = df_merged[df_merged["Risk"] == 1].shape[0]
        nsCount = df_merged[df_merged["NS Alerts"] == 1].shape[0]

        col1, col2 = st.columns(2)
        col1.subheader("Vito Alerts: " + str(vitoCount))
        vitoTotal["vitoTotal"] += vitoCount
        col2.subheader("NightSignal Alerts: " + str(nsCount))
        nsTotal["nsTotal"] += nsCount

        df_merged["correct"] = df_merged["Risk"] == df_merged["NS Alerts"]

        all["all"] = pd.concat([all["all"], df_merged])
        accuracy = sum(df_merged["correct"] / len(df_merged["correct"]))

        if df_merged.shape[0] > 5:
            averages["averages"].append(accuracy_score(
                df_merged["Risk"], df_merged["NS Alerts"]))
            kap = cohen_kappa_score(df_merged["Risk"], df_merged["NS Alerts"])
            recall = recall_score(df_merged["Risk"], df_merged["NS Alerts"])
            precision = precision_score(
                df_merged["Risk"], df_merged["NS Alerts"])

            if pd.notna(kap):
                kappaArr["kappa"].append(kap)
                ["kappa"].append(kap)
                precisionArr["precision"].append(precision)
                recallArr["recall"].append(recall)
                st.header(kap)
        df_merged.to_csv(os.path.join("/tmp/Vito_Alert_Statistics.csv"))

        with open(os.path.join("/tmp/Vito_Alert_Statistics.csv"), "rb") as file:
            st.download_button(
                "Download Alert Statistics",
                file,
                file_name=os.path.join("/tmp/Vito_Alert_Statistics.csv"),
                on_click=st.balloons,
            )
        with st.expander("See full data"):
            col, col2 = st.columns(2)
            st.table(df_merged)

        df = DataFrame()
        df.insert(0, "Start_Date_Risk", allDates, True)
        df.insert(0, "Value", allAlertVals, True)



    def file_selector(folder_path='./sample_data/', type="Health3"):
        folder_path = folder_path + type
        filenames = os.listdir(folder_path)
        csvFiles = []
        for file in filenames:
            if "csv" in file:
                csvFiles.append(file)
        selected_filename = st.selectbox('Select ' + type, csvFiles)
        return os.path.join(folder_path, selected_filename)

    def processAll(folder_path='../sample_data_from_main/', type="Healthv6v2"):
        folder_path = folder_path + type
        filenames = os.listdir(folder_path)
        csvFiles = []
        for file in filenames:
            if "csv" in file:

                try:
                    processData(os.path.join(folder_path, file))
                except:
                    print()
    analysis()
    if st.button("Process All"):
        processAll(type="Healthv8")
        col1, col2 = st.columns(2)

        col1.subheader("Vito Alerts: " + str(vitoTotal))

        col2.subheader("NightSignal Alerts: " + str(nsTotal))

        allDF = all["all"]

        st.sidebar.header(
            "Accuracy: " + str(accuracy_score(allDF["Risk"], allDF["NS Alerts"])))
        st.sidebar.header(
            "Kappa: " + str(cohen_kappa_score(allDF["Risk"], allDF["NS Alerts"])))
        st.sidebar.header(
            "Precision: " + str(precision_score(allDF["Risk"], allDF["NS Alerts"])))
        st.sidebar.header(
            "Recall: " + str(recall_score(allDF["Risk"], allDF["NS Alerts"])))
