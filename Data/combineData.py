import os

import pandas as pd


def file_selector(folder_path='./COVID-19-Phase2-Wearables'):
        df = pd.DataFrame()
        folder_path = folder_path 
        filenames = os.listdir(folder_path)
        csvFiles = []
        count = 0
        for file in filenames:
            try:
               
                
                
                currentPath = (folder_path + "/" + file + "/" + "Orig_NonFitbit_HR.csv")
                #df = df.append(pd.read_csv(folder_path + "/" + file + "/" + "Orig_NonFitbit_HR.csv", skiprows=0))
                # df.to_csv("./all.csv")
                os.replace(currentPath, "./COVID-19-Phase2-Wearables" + "/Data/Orig_NonFitbit_HR" + count + ".csv")
                count += 1
            except:
                print()
        return df
                #csvFiles.append(file)


file_selector()
        #selected_filename = st.selectbox('Select ' + type, csvFiles)
       # return os.path.join.join(folder_path, selected_filename)

