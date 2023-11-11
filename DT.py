import streamlit as st
import pandas as pd
import joblib
model = joblib.load('model.pkl')
encoder = joblib.load('encoder.pkl')

st.title("GVHD")
# User input fields
st.sidebar.header("User Input")

# Define input fields for the variables you provided
st.sidebar.subheader("User Input Variables")
Recipientgender = st.sidebar.radio("Recipient gender",["Male","Female"])
Donorage = st.sidebar.slider("Donor age", min_value=0, max_value=100, value=50, step=1)
Riskgroup = st.sidebar.radio("Risk group",["High risk","Low risk"])
HLAmatch = st.sidebar.selectbox("HLA match",[10/10,9/10,8/10])
Allele = st.sidebar.selectbox(" Allele",["No difference" ,"One difference"," Two difference"])
Recipientage  = st.sidebar.slider("Recipient age", min_value=0, max_value=100, value=50, step=1)
CD34kgx10d6 = st.sidebar.slider("CD34kgx10d6", min_value=0, max_value=100, value=50, step=1)

def preprocess_user_input(user_input, encoder):
    # Create a copy of the user input
    user_input_encoded = user_input.copy()
    

    # Make sure that categorical columns are of 'category' dtype
    user_input_encoded[categorical_columns] = user_input_encoded[categorical_columns].astype('category')

    # Apply the encoder to the categorical columns
    user_input_encoded[categorical_columns] = encoder.transform(user_input_encoded[categorical_columns])

    return user_input_scaled

if st.sidebar.button("Predict IIIV"):
    user_input = pd.DataFrame({
        'Recipientgender': [Recipientgender],
        'Donorage' : [Donorage],
        'Riskgroup' : [Riskgroup],
        'HLAmatch' : [HLAmatch],
        'Allele' : [Allele],
        'Recipientage' :[Recipientage],
        'CD34kgx10d6':[CD34kgx10d6]
    })
    categorical_columns = ['Recipientgender','Riskgroup','HLAmatch','Allele']
    user_input[categorical_columns] = user_input[categorical_columns].astype('category')
    user_input_values = user_input.values.flatten()
    user_input_encoded = encoder.transform(user_input)


    # Make a prediction using your loaded SVM model
    prediction = model.predict(user_input_encoded.reshape(1, -1))
    


    # Display the prediction result
    st.sidebar.subheader("Prediction (IIIV)")
    st.sidebar.write("The predicted class for IIIV is:", prediction[0])

