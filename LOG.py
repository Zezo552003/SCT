import pandas as pd
import joblib
import streamlit as st

# Load the trained model and encoder
model = joblib.load(final.pkl')
encoder = joblib.load(encoder.pkl')

st.title("GVHD Prediction")
st.image('bloodstemcell.jpg', use_column_width=True)  # Replace "path_to_your_image.jpg" with the actual path to your image
# User input fields
st.header("User Input")

# Define input fields for the variables you provided
st.subheader("User Input Variables")
Recipientgender = st.radio("Recipient gender", ['Male', 'Female'])
Donorage = st.slider("Donor age", min_value=0, max_value=100, value=50, step=1)
Riskgroup = st.radio("Risk group", ['High risk', 'Low risk'])
HLAmatch = st.selectbox("HLA match", ['10/10', '9/10', '8/10'])
Allele = st.selectbox("Allele", ['No difference', 'One difference', 'Two difference'])
Recipientage = st.slider("Recipient age", min_value=0, max_value=100, value=50, step=1)
CD34kgx10d6 = st.slider("CD34kgx10d6", min_value=0, max_value=100, value=50, step=1)

def preprocess_user_input(user_input, encoder):
    # Create a copy of the user input
    user_input_encoded = user_input.copy()

    # Define label encoding mappings

    label_encodings = {
        'Riskgroup': {'High risk': 1, 'Low risk': 0},
        'HLAmatch': {'10/10': 0, '9/10': 1, '8/10': 2},
        'Allele': {'No difference': 0, 'One difference': 1, 'Two difference': 2},
        'Recipientgender': {'Male': 1, 'Female': 0}
    }

    # Apply label encoding to the categorical columns
    for column, encoding in label_encodings.items():
        user_input_encoded[column] = user_input_encoded[column].map(encoding)

    return user_input_encoded

if st.button("Predict GVHD"):
    user_input = pd.DataFrame({
        'Recipientgender': [Recipientgender],
        'Donorage': [Donorage],
        'Riskgroup': [Riskgroup],
        'HLAmatch': [HLAmatch],
        'Allele': [Allele],
        'Recipientage': [Recipientage],
        'CD34kgx10d6': [CD34kgx10d6]
    })
  # Probability for class 1 (positive class)


    user_input_encoded = preprocess_user_input(user_input, encoder)
    class_probabilities = model.predict_proba(user_input_encoded)


    # Make a prediction using your loaded SVM model
    prediction = model.predict(user_input_encoded)


    st.write("GVHD Prediction:", prediction)
    st.write("Class Probabilities:", class_probabilities)
    if prediction[0] == 'Yes':
        st.write("The patient is at high risk of developing GVHD.")
    else:
        st.write("The patient is at low risk of developing GVHD.")
    probability_percentage = class_probabilities[0][1] * 100
    st.write("Probability to get GVHD:", f"{probability_percentage:.2f}%")


