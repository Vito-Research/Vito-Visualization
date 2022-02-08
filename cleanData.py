import pandas as pd 
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from pathlib import Path
import pickle
def train_model(train_features, train_labels, test_features, test_lables):
    # Instantiate model
    n_estimators = 1000
    random_state = 42
    reg_model = RandomForestRegressor(
        n_estimators=n_estimators, random_state=random_state
    )
    class_model = RandomForestClassifier(
        n_estimators=n_estimators, random_state=random_state
    )

    # Train the models on training data
    reg_model.fit(train_features, train_labels)
    class_model.fit(train_features, train_labels)

    # Use the forest's predict method on the test data
    reg_pred = reg_model.predict(test_features)
    st.write(reg_pred)
    class_pred = class_model.predict(test_features)
    reg_metrics(reg_pred, [1])
    get_importances(reg_model, "regression", ["value_x", "value_y"])
    return reg_model, reg_pred, class_model, class_pred
def reg_metrics(predictions, test_labels):
        # Calculate the absolute errors
        errors = abs(predictions - test_labels)
        print("Regression mean error:", round(np.mean(errors), 2))
        st.header("Regression mean error:", round(np.mean(errors), 2))
def get_importances(model, model_name, feature_list):
        # Get numerical feature importances
        importances = list(model.feature_importances_)

        # List of tuples with variable and importance
        feature_importances = [
            (feature, round(importance, 2))
            for feature, importance in zip(feature_list, importances)
        ]

        # Sort the feature importances by most important first
        feature_importances = sorted(
            feature_importances, key=lambda x: x[1], reverse=True
        )

        # Print out the feature and importances
        print(f"Feature importances for {model_name}: ")
        [
            st.write("Variable: {:20} Importance: {}".format(*pair))
            
            for pair in feature_importances
        ]
hrvDf = pd.read_csv("./Data/HRV2.csv")
respiratoryDf = pd.read_csv("./Data/Respiratory2.csv")



hrvDf["date"] = pd.to_datetime(hrvDf["startDate"]).round("120min")

respiratoryDf["date"] = pd.to_datetime(respiratoryDf["startDate"]).round("120min")
vaccine = hrvDf.groupby('date')["Vaccine"].median()
hrvDf = hrvDf.groupby('date')["value"].median()
respiratoryDf = respiratoryDf.groupby('date')["value"].median()
mergedDf = pd.merge(respiratoryDf, hrvDf, how='outer', on ='date')
mergedDf2 = pd.merge(mergedDf, vaccine, how='outer', on ='date')
mergedDf2 = mergedDf2[mergedDf2[['value_x', 'value_y', 'Vaccine']].notnull().all(1)]
st.table(mergedDf2)
mergedDf2.to_csv("Combined.csv")
labels = np.array(mergedDf2["Vaccine"])
train_features, test_features, train_labels, test_labels = train_test_split(
        mergedDf2, labels, test_size=0.25, random_state=42
    )

train_model(
        train_features, train_labels, test_features, test_labels
    )