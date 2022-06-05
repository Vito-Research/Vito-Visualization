import pandas as pd
import datetime
import streamlit as st


# TODO: update to not define global variables outside of analyze function
# Tuesday, March 22
daysBefore = -5

date_time_str = "2022-03-22 00:00:00.243860"
date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f").date()


def analyze(file, unit):
    df = pd.read_excel("./sample_data/" + file + ".xlsx")
    df["startTime"] = pd.to_datetime(df["startDate"]).dt.hour
    df["startDate"] = pd.to_datetime(df["startDate"]).dt.date
    df["startWeek"] = pd.to_datetime(df["startDate"]).dt.week

    # aWeekAgo = pd.to_datetime(datetime.datetime.now() + datetime.timedelta(days= daysBefore))
    aWeekAgo = date_time_obj
    dfBeforeSick = df[df["startDate"] < aWeekAgo]

    dfAfterSick = df[df["startDate"] > aWeekAgo]
    df = df[df["startWeek"] < 14]
    df = df[df["startWeek"] > 3]
    print(unit + " Before Sick: " + str(dfBeforeSick["value"].median()))
    print(unit + " Three days prior to symptoms: " + str(dfAfterSick["value"].median()))

    groupedByWeek = df.groupby(df["startWeek"])["value"].median()
    arr = pd.Series([dfBeforeSick["value"].median(), dfAfterSick["value"].median()])
    precentChanged = arr.pct_change()[1] * 100
    st.metric("Heart Rate", dfAfterSick["value"].median(), precentChanged)
    st.line_chart(groupedByWeek)


def analysis():
    choice = st.selectbox(
        "Data to Analyze", ["Heart Rate", "Respiration Rate", "Heart Rate Varability"]
    )
    st.caption(
        "Data was collected from Andreas Ink, the lead of Vito, who began showing symptoms of a non-covid respiratory illness (tested negitive for Covid-19 twice) on week 12.  This is by no means formal data, simply an interesting statistic."
    )
    if choice == "Heart Rate":
        analyze("HRData", "HR")
    if choice == "Respiration Rate":
        analyze("RRData", "RR")
    if choice == "Heart Rate Varability":
        analyze("HRVData", "HRV")


# -- Execution -- #
analysis()
