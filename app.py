import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
st.set_page_config(
    page_title="Health Prediction App",
    page_icon="🏥",
    layout="wide")
conn = sqlite3.connect("patients.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT,
    email TEXT,
    glucose REAL,
    haemoglobin REAL,
    cholesterol REAL,
    remarks TEXT
)
""")

conn.commit()
from sklearn.tree import DecisionTreeClassifier

X = [[80,14,150],
    [90,15,160],
    [180,11,250],
    [200,10,280],
    [220,9,300]
]

y = [
    "Healthy",
    "Healthy",
    "Diabetes Risk",
    "Diabetes Risk",
    "High Risk"
]

model = DecisionTreeClassifier()
model.fit(X, y)
def ai_remark(glucose, cholesterol):
    if glucose > 180:
        return "AI Risk: High Diabetes Risk"
    elif cholesterol > 240:
        return "AI Risk: High Cholesterol Risk"
    else:
        return "AI Risk: Normal Health"

st.title("🏥 Health Prediction Application")
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Patient",
        "View Patients",
        "Update Patient",
        "Delete Patient"
    ]
)
if menu == "Add Patient":

    name = st.text_input("Full Name")

    dob = st.date_input(
        "Date of Birth",
        max_value=date.today()
    )

    email = st.text_input("Email Address")

    glucose = st.number_input(
        "Glucose",
        min_value=0.0
    )

    haemoglobin = st.number_input(
        "Haemoglobin",
        min_value=0.0
    )

    cholesterol = st.number_input(
        "Cholesterol",
        min_value=0.0
    )

    if st.button("Add Patient"):

        if name.strip() == "":
            st.error("Name cannot be empty")

        elif email.strip() == "":
            st.error("Email cannot be empty")

        elif "@" not in email:
            st.error("Invalid email format")

        elif glucose <= 0 or haemoglobin <= 0 or cholesterol <= 0:
            st.error("Values must be greater than 0")

        else:
            prediction = model.predict(
                [[glucose, haemoglobin, cholesterol]]
            )[0]

            ai_result = ai_remark(
                glucose,
                cholesterol
            )

            final_remark = (
                prediction + " | " + ai_result
            )

            cursor.execute("""
            INSERT INTO patients
            (name, dob, email, glucose,
            haemoglobin, cholesterol, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                str(dob),
                email,
                glucose,
                haemoglobin,
                cholesterol,
                final_remark
            ))

            conn.commit()

            st.success(
                "Patient Added Successfully"
            )

            st.balloons()

elif menu == "View Patients":

    df = pd.read_sql_query(
        "SELECT * FROM patients",
        conn
    )

    st.dataframe(df)
elif menu == "Update Patient":

    patient_id = st.number_input(
        "Patient ID",
        min_value=1,
        step=1
    )

    new_email = st.text_input(
        "New Email Address"
    )

    if st.button("Update Email"):

        cursor.execute("""
        UPDATE patients
        SET email = ?
        WHERE id = ?
        """,
        (new_email, patient_id))

        conn.commit()

        st.success(
            "Email Updated Successfully"
        )


elif menu == "Delete Patient":

    patient_id = st.number_input(
        "Patient ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Patient"):

        cursor.execute("""
        DELETE FROM patients
        WHERE id = ?
        """,
        (patient_id,))

        conn.commit()

        st.success(
            "Patient Deleted Successfully"
        )
