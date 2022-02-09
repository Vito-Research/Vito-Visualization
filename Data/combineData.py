import pandas as pd
import os
import streamlit as st
def file_selector(folder_path='./COVID-19-Phase2-Wearables'):
        df = pd.DataFrame()
        folder_path = folder_path 
        filenames = os.listdir(folder_path)
        csvFiles = []

        for file in filenames:
            try:
               
                
                
                print(folder_path + "/" + file + "/" + "Orig_NonFitbit_HR.csv")
                df = df.append(pd.read_csv(folder_path + "/" + file + "/" + "Orig_NonFitbit_HR.csv", skiprows=0))
                df.to_csv("./all.csv")
            except:
                print()
        return df
                #csvFiles.append(file)


file_selector()
        #selected_filename = st.selectbox('Select ' + type, csvFiles)
       # return os.path.join(folder_path, selected_filename)

