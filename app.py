# app.py

import streamlit as st
import requests

st.title("Heart Disease Predictor")

features = []
labels = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
          'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

for label in labels:
    value = st.number_input(f"Enter {label}", step=1.0)
    features.append(value)

if st.button("Predict"):
    # Replace with your Railway public URL
    url = "https://your-railway-url.up.railway.app/predict"
    response = requests.post(url, json={"features": features})
    prediction = response.json()["prediction"]

    if prediction == 1:
        st.success("🚨 Patient is likely to have heart disease.")
    else:
        st.success("✅ Patient is unlikely to have heart disease.")