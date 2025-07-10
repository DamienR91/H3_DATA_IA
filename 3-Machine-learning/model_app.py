import streamlit as st
import joblib

model = joblib.load("regression.joblib")

st.title("Estimation du prix d'une maison")

taille = st.number_input("Taille de la maison (m²)", min_value=10, max_value=1000, value=50)
nb_chambres = st.number_input("Nombre de chambres", min_value=1, max_value=20, value=3)
jardin = st.number_input("Jardin (0 = non, 1 = oui)", min_value=0, max_value=1, value=0)

if st.button("Prédire le prix"):
    X_new = [[taille, nb_chambres, jardin]]
    prediction = model.predict(X_new)
    st.write(f"Le prix estimé de la maison est : {prediction[0]:.2f} €")

