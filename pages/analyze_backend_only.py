import json
import os

import pandas as pd
from pandas.core.frame import DataFrame
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from vito_algorithms import nightsignal as ns

# import analysis


def add_blank_rows(df, no_rows):
    df_new = pd.DataFrame(columns=df.columns)
    for idx in range(len(df)):
        df_new = df_new.append(df.iloc[idx])
        for _ in range(no_rows):
            df_new = df_new.append(pd.Series(), ignore_index=True)
    return df_new


def analyze():

    # dictionaries for single var ?
    ns_total = {"ns_total": 0}
    vitoTotal = {"vitoTotal": 0}
    matchingTotal = {"matchingTotal": 0}  # unused var
    averages = {"averages": []}
    kappaArr = {"kappa": []}
    precisionArr = {"precision": []}
    recallArr = {"recall": []}

    all = {"all": pd.DataFrame()}

    # [UI]
    # st.header("Add Your File")
    # HRFile = st.file_uploader("Upload Heartrate Data", type="csv")
    HRFile = "/Users/ethancloin/PycharmProjects/Vito-Visualization/sample_data/Healthv6v2/Vito_Health_Data0.csv"
    HRFileName = ""  # unused var
    RiskFileName = ""  # unused var

    def processData(HRFile):

        # read csv file into dataframe and store in tmp directory
        provided_hr_data = pd.read_csv(HRFile)
        provided_hr_data.to_csv(os.path.join("/tmp/tmp.csv"))
        count = provided_hr_data.shape[0]

        # devices = []
        # for i in range(count):
        #     devices.append("HK Apple Watch")
        devices = ["HK Apple Watch" for _ in range(count)]
        provided_hr_data.insert(0, "Device", devices, True)

        # i = 0
        # steps = []
        # start_time = []
        # end_time = []
        # end_date = []
        # start_date = []
        # dfSteps = DataFrame()
        # dfSteps.insert(0, "Steps", steps, True)
        # dfSteps.insert(0, "Start_Date", start_date, True)
        # dfSteps.insert(0, "Start_Time", start_time, True)
        # dfSteps.insert(0, "End_Date", start_date, True)
        # dfSteps.insert(0, "End_Time", end_time, True)

        # creating empty dataframe with given col names
        step_data = pd.DataFrame(
            columns=["Steps", "Start_Date", "Start_Time", "End_Date", "End_Time"]
        )

        tmp_step_file = "/tmp/tmp2.csv"
        step_data.to_csv(os.path.join(tmp_step_file))

        # [UI]
        # col1, col2, col3 = st.columns(3)

        # TODO: ns.getScore writes to /tmp/NS-signals.json, consider refactoring
        #   to returning a json string or dict instead
        ns.getScore(os.path.join("/tmp/tmp.csv"), tmp_step_file)

        # deleting
        ns_output_json = "/tmp/NS-signals.json"
        with open(os.path.join(ns_output_json), "r") as f:
            ns_output: dict = json.load(f)
            # os.system("rm " + os.path.join(ns_output_json))
            # os.system("rm " + os.path.join("/tmp/tmp.csv"))
            os.remove(os.path.join(ns_output_json))
            os.remove(os.path.join("/tmp/tmp.csv"))

        ns_alerts = ns_output["nightsignal"]

        # HRFile is a required param, will never be None
        # if HRFile is not None:
        # high_alert_vals = []
        # all_alert_vals = []
        # all_dates = []
        #
        # for alert in ns_alerts:
        #     all_alert_vals.append(alert["val"])
        #     all_dates.append(alert["date"])
        #     if int(alert["val"]) > 1:
        #         high_alert_vals.append(alert["val"])
        all_alert_vals = [alert["val"] for alert in ns_alerts]
        alert_dates = [alert["date"] for alert in ns_alerts]
        high_alert_vals = [val for val in all_alert_vals if int(val) > 1]

        nsAlertCount = len(high_alert_vals)  # unused var
        vitoAlertCount = len(
            provided_hr_data[provided_hr_data["Risk"] > 0.9]
        )  # unused var

        # [UI]
        # col1, col2 = st.columns(2)

        newDates = []
        newAlerts = []
        df2 = DataFrame()
        for i in range(len(all_dates)):

            targetDates = []
            for date in provided_hr_data["Start_Date"]:
                targetDates.append(date)

            if all_dates[i] in targetDates:
                newDates.append(all_dates[i])
                newAlerts.append(all_alert_vals[i])

        df2.insert(0, "Start_Date_Risk", newDates, True)
        df2.insert(0, "NS Alerts", newAlerts, True)
        df2["NS Alerts"] = df2["NS Alerts"].replace(to_replace="1", value="0")
        df2["NS Alerts"] = df2["NS Alerts"].replace(to_replace="2", value="1")

        provided_hr_data["Risk"] = provided_hr_data["Risk"].astype(int)
        df2["NS Alerts"] = df2["NS Alerts"].astype(int)
        df2.rename(columns={"Start_Date_Risk": "Start_Date"}, inplace=True)
        provided_hr_data["Start_Date"] = pd.to_datetime(provided_hr_data["Start_Date"])
        df2["Start_Date"] = pd.to_datetime(df2["Start_Date"])
        df_merged = pd.merge(provided_hr_data, df2, how="inner", on="Start_Date")

        df_merged = df_merged.dropna()
        provided_hr_data = provided_hr_data.drop("Heartrate", 1)
        provided_hr_data = provided_hr_data.drop("Start_Time", 1)
        provided_hr_data = provided_hr_data.drop("Device", 1)
        column_names = ["Risk", "Start_Date"]  # unused var

        count = df2.shape[0] - provided_hr_data.shape[0]  # unused var

        vitoCount = df_merged[df_merged["Risk"] == 1].shape[0]
        ns_count = df_merged[df_merged["NS Alerts"] == 1].shape[0]

        # [UI]
        # col1, col2 = st.columns(2)
        # col1.subheader("Vito Alerts: " + str(vitoCount))
        vitoTotal["vitoTotal"] += vitoCount
        # col2.subheader("NightSignal Alerts: " + str(ns_count))
        ns_total["ns_total"] += ns_count

        df_merged["correct"] = df_merged["Risk"] == df_merged["NS Alerts"]

        all["all"] = pd.concat([all["all"], df_merged])

        # unused var (seems important)
        accuracy = sum(df_merged["correct"] / len(df_merged["correct"]))

        # what does it signify if this shape[0] is > 5 ?
        if df_merged.shape[0] > 5:
            averages["averages"].append(
                accuracy_score(df_merged["Risk"], df_merged["NS Alerts"])
            )
            kap = cohen_kappa_score(df_merged["Risk"], df_merged["NS Alerts"])
            recall = recall_score(df_merged["Risk"], df_merged["NS Alerts"])
            precision = precision_score(df_merged["Risk"], df_merged["NS Alerts"])

            if pd.notna(kap):
                kappaArr["kappa"].append(kap)
                ["kappa"].append(kap)
                precisionArr["precision"].append(precision)
                recallArr["recall"].append(recall)

                # [UI]
                # st.header(kap)
        df_merged.to_csv(os.path.join("/tmp/Vito_Alert_Statistics.csv"))

        # [UI]
        # with open(os.path.join("/tmp/Vito_Alert_Statistics.csv"), "rb") as file:
        #     st.download_button(
        #         "Download Alert Statistics",
        #         file,
        #         file_name=os.path.join("/tmp/Vito_Alert_Statistics.csv"),
        #         on_click=st.balloons,
        #     )
        # with st.expander("See full data"):
        #     col, col2 = st.columns(2)
        #     st.table(df_merged)

        provided_hr_data = DataFrame()
        provided_hr_data.insert(0, "Start_Date_Risk", all_dates, True)
        provided_hr_data.insert(0, "Value", all_alert_vals, True)

    if HRFile is not None:
        processData(HRFile)

    # def file_selector(folder_path="./sample_data/", type="Health3"):
    #     folder_path = folder_path + type
    #     filenames = os.listdir(folder_path)
    #     csvFiles = []
    #     for file in filenames:
    #         if "csv" in file:
    #             csvFiles.append(file)
    #     # selected_filename = st.selectbox("Select " + type, csvFiles)
    #     return os.path.join(folder_path, selected_filename)

    def processAll(folder_path="../sample_data_from_main/", type="Healthv6v2"):
        folder_path = folder_path + type
        filenames = os.listdir(folder_path)
        csvFiles = []
        for file in filenames:
            if "csv" in file:

                try:
                    processData(os.path.join(folder_path, file))
                except:
                    print()

    # analysis()
    # if st.button("Process All"):
    COND = True
    if COND:
        processAll(type="Healthv8")
        # col1, col2 = st.columns(2)

        # col1.subheader("Vito Alerts: " + str(vitoTotal))

        # col2.subheader("NightSignal Alerts: " + str(ns_total))

        allDF = all["all"]
        # four accuracy scores
        print(str(accuracy_score(allDF["Risk"], allDF["NS Alerts"])))
        print(str(cohen_kappa_score(allDF["Risk"], allDF["NS Alerts"])))
        print(str(cohen_kappa_score(allDF["Risk"], allDF["NS Alerts"])))
        print(str(recall_score(allDF["Risk"], allDF["NS Alerts"])))
        # st.sidebar.header(
        #     "Accuracy: " + str(accuracy_score(allDF["Risk"], allDF["NS Alerts"]))
        # )
        # st.sidebar.header(
        #     "Kappa: " + str(cohen_kappa_score(allDF["Risk"], allDF["NS Alerts"]))
        # )
        # st.sidebar.header(
        #     "Precision: " + str(precision_score(allDF["Risk"], allDF["NS Alerts"]))
        # )
        # st.sidebar.header(
        #     "Recall: " + str(recall_score(allDF["Risk"], allDF["NS Alerts"]))
        # )


# -- Execution -- #
analyze()
