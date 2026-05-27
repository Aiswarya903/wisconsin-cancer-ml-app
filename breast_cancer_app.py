import streamlit as st
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB

# Title
st.title("Breast Cancer Prediction App")
st.write("Enter tumor measurements below to predict if it's benign or malignant.")

# Load dataset
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

# Use only any 4 features for simplicity
selected_features = list(X.columns[3:7])
X = X[selected_features]

# Split and scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train) 

# Train Naive Bayes model
model = GaussianNB()
model.fit(X_train_scaled, y_train)

# Input fields
user_input = []  #used to collect input through streamlit
for feature in selected_features:   #input box gets created
    value = st.number_input(f"{feature}", min_value=0.0, format="%.5f") #float values can be given as input
    user_input.append(value) #collect each input into list

# Prediction button
if st.button("Predict"):
    input_df = pd.DataFrame([user_input], columns=selected_features)
    input_scaled = scaler.transform(input_df) #scaling on user input
    prediction = model.predict(input_scaled)[0] #predict the class
    probabilities = model.predict_proba(input_scaled)[0]
    confidence = round(max(probabilities) * 100, 2) #highest probability value is shown here
    result = "Benign(Non-cancerous)" if prediction == 1 else "Malignant(Cancerous)"
    st.success(f"Prediction: **{result}** with {confidence}% confidence")  #displays result


