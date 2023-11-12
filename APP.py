import streamlit as st
import pandas as pd
import joblib

# Load your trained model, MinMaxScaler, and Label Encoder
model = joblib.load(r'c:\\Users\\ascom\\AppData\\Local\\Programs\\Microsoft VS Code\\svc_model.pkl')

scaler = joblib.load('scaler.pkl')
encoder = joblib.load(r'c:\\Users\\ascom\\AppData\\Local\\Programs\\Microsoft VS Code\\label_encoder.pkl')

# Create the Streamlit app
st.title("SVM Classifier Web App")

# User input fields
st.sidebar.header("User Input")

# Define input fields for the variables you provided
st.sidebar.subheader("User Input Variables")

# Define input fields based on the role and type of each variable
recipientgender = st.sidebar.radio("Recipientgender (Male - 1, Female - 0)", [1, 0])
stemcellsource = st.sidebar.radio("Stemcellsource (Peripheral blood - 1, Bone marrow - 0)", [1, 0])
donorage = st.sidebar.slider("Donorage (Age of donor)", 0, 100, 50)
donorage35 = st.sidebar.radio("Donorage35 (Donor age <35 - 0, Donor age >=35 - 1)", [0, 1])

gendermatch = st.sidebar.radio("Gendermatch (Compatibility of donor and recipient according to gender - Female to Male: 1, Other: 0)", [1, 0])
donorabo = st.sidebar.selectbox("DonorABO (ABO blood group of the donor of hematopoietic stem cells)", [0, 1, -1, 2])
recipientabo = st.sidebar.selectbox("RecipientABO (ABO blood group of the recipient of hematopoietic stem cells)", [0, 1, -1, 2])
recipientrh = st.sidebar.radio("RecipientRh (Presence of the Rh factor on recipient's red blood cells - '+': 1, '-': 0)", [1, 0])
abomatch = st.sidebar.radio("ABOmatch (Compatibility of donor and recipient according to ABO blood group - Matched: 1, Mismatched: 0)", [1, 0])
cmvstatus = st.sidebar.selectbox("CMVstatus (Serological compatibility of donor and recipient according to cytomegalovirus)", [0, 3])
donorcmv = st.sidebar.radio("DonorCMV (Presence of cytomegalovirus infection in the donor of hematopoietic stem cells prior to transplantation - Present: 1, Absent: 0)", [1, 0])
recipientcmv = st.sidebar.radio("RecipientCMV (Presence of cytomegalovirus infection in the donor of hematopoietic stem cells prior to transplantation - Presence: 1, Absence: 0)", [1, 0])

riskgroup = st.sidebar.radio("Riskgroup (High risk: 1, Low risk: 0)", [1, 0])
txpostrelapse = st.sidebar.radio("Txpostrelapse (The second bone marrow transplantation after relapse - Yes: 1, No: 0)", [1, 0])
diseasegroup = st.sidebar.radio("Diseasegroup (Type of disease - Malignant: 1, Nonmalignant: 0)", [1, 0])
hlamatch = st.sidebar.selectbox("HLAmatch (Compatibility of antigens of the main histocompatibility complex of the donor and the recipient according to ALL international BFM SCT 2008 criteria)", [0, 1, 2, 3])
hlamismatch = st.sidebar.radio("HLAmismatch (HLA matched: 0, HLA mismatched: 1)", [0, 1])
antigen = st.sidebar.selectbox("Antigen (In how many antigens there is a difference between the donor and the recipient)", [-1, 0, 1, 2, 3])
allele = st.sidebar.selectbox("Allele (In how many alleles there is a difference between the donor and the recipient)", [-1, 0, 1, 2, 3])
hlagri = st.sidebar.selectbox("HLAgrI (The difference type between the donor and the recipient)", [0, 1, 2, 3, 4, 5])
recipientage = st.sidebar.slider("Recipientage (Age of the recipient at the time of transplantation)", 0, 100, 50)
recipientage10 = st.sidebar.radio("Recipientage10 (Recipient age <10: 0, Recipient age >=10: 1)", [0, 1])
recipientageint = st.sidebar.selectbox("Recipientageint (Recipient age in age groups)", [0, 1, 2])
relapse = st.sidebar.radio("Relapse (Reoccurrence of the disease - No: 0, Yes: 1)", [0, 1])
cd34kgx10d6 = st.sidebar.slider("CD34+ cell dose per kg of recipient body weight (10^6/kg)", 0.0, 10.0, 7.2)
cd3dcd34 = st.sidebar.slider("CD3+ cell to CD34+ cell ratio", 0.0, 2.0, 1.33876)
cd3dkgx10d8 = st.sidebar.slider("CD3+ cell dose per kg of recipient body weight (10^8/kg)", 0.0, 10.0, 5.38)
rbodymass = st.sidebar.slider("Body mass of the recipient", 0.0, 100.0, 35.0)
ancrecovery = st.sidebar.slider("Time to neutrophils recovery (in days)", 0, 100, 19)
pltrecovery = st.sidebar.slider("Time to platelet recovery (in days)", 0, 100, 51)

# Define a function to preprocess user input
def preprocess_user_input(user_input, scaler, encoder):
    # Create a copy of the user input
    user_input_encoded = user_input.copy()
    

    # Make sure that categorical columns are of 'category' dtype
    user_input_encoded[categorical_columns] = user_input_encoded[categorical_columns].astype('category')

    # Apply the encoder to the categorical columns
    user_input_encoded[categorical_columns] = encoder.transform(user_input_encoded[categorical_columns])

    # Scale the data
    user_input_scaled = scaler.transform(user_input_encoded)

    return user_input_scaled

# Prediction based on user input
if st.sidebar.button("Predict IIIV"):
    # Prepare user input as a DataFrame
    user_input = pd.DataFrame({
        'Recipientgender': [recipientgender],
        'Stemcellsource': [stemcellsource],
        'Donorage': [donorage],
        'Donorage35': [donorage35],
        
        'Gendermatch': [gendermatch],
        'DonorABO': [donorabo],
        'RecipientABO': [recipientabo],
        'RecipientRh': [recipientrh],
        'ABOmatch': [abomatch],
        'CMVstatus': [cmvstatus],
        'DonorCMV': [donorcmv],
        'RecipientCMV': [recipientcmv],
        
        'Riskgroup': [riskgroup],
        'Txpostrelapse': [txpostrelapse],
        'Diseasegroup': [diseasegroup],
        'HLAmatch': [hlamatch],
        'HLAmismatch': [hlamismatch],
        'Antigen': [antigen],
        'Allele': [allele],
        'HLAgrI': [hlagri],
        'Recipientage': [recipientage],
        'Recipientage10': [recipientage10],
        'Recipientageint': [recipientageint],
        'Relapse': [relapse],
        'CD34kgx10d6': [cd34kgx10d6],
        'CD3dcd34': [cd3dcd34],
        'CD3dkgx10d8': [cd3dkgx10d8],
        'Rbodymass': [rbodymass],
        'ANCrecovery': [ancrecovery],
        'PLTrecovery': [pltrecovery],
    })
    

    categorical_columns = [
    'Recipientgender', 'Stemcellsource', 'Donorage35', 'Gendermatch',
    'DonorABO', 'RecipientABO', 'RecipientRh', 'ABOmatch', 'CMVstatus',
    'DonorCMV', 'RecipientCMV', 'Riskgroup', 'Txpostrelapse',
    'Diseasegroup', 'HLAmatch', 'HLAmismatch', 'Antigen', 'Allele', 'HLAgrI',
    'Recipientage10', 'Relapse',
]
    user_input[categorical_columns] = user_input[categorical_columns].astype('category')
    user_input_values = user_input.values.flatten()
    user_input_encoded = encoder.transform(user_input)

    # Scale the data
    user_input_scaled = scaler.transform(user_input_encoded)

    # Make a prediction using your loaded SVM model
    prediction = model.predict(user_input_encoded.reshape(1, -1))
    


    # Display the prediction result
    st.sidebar.subheader("Prediction (IIIV)")
    st.sidebar.write("The predicted class for IIIV is:", prediction[0])
