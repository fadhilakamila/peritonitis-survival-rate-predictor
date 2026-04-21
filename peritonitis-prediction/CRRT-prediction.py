import streamlit as st
import pandas as pd
import hmac
from datetime import datetime
# from streamlit_gsheets import GSheetsConnection

def check_password():

    def login_form():
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Login", on_click=password_entered)
    
    def password_entered():
        if st.session_state["username"] in st.secrets["password"] and hmac.compare_digest(st.session_state["password"], st.secrets["password"][st.session_state["username"]]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
    
    if st.session_state.get("password_correct", False):
        return True
    
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 Incorrect username or password.")
    return False

if not check_password():
    st.stop()
            
st.set_page_config(
    page_title="Predict CRRT for Kids",
    page_icon=":hospital:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

#AppVersion: 2.0

@st.cache_data
def load_data():
    file_path = 'D:\\Kuliah\\TA\\Mas Zulfan\\crrt-prediction\\PredictCRRTforKids_Database.xlsx'
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Error: File data lokal '{file_path}' tidak ditemukan. Pastikan file ada di folder yang sama dengan app.py.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca data: {e}")
        return pd.DataFrame()

def main():
    df = load_data()

    if df.empty:
        st.warning("Aplikasi tidak dapat berjalan karena data gagal dimuat.")
        return # Menghentikan eksekusi main() jika data kosong

    st.title("Pediatric CRRT Calculator for Survival Prediction (PCCSP)")
    with st.sidebar:
        st.write("Credits")
        st.write("Developed by: **Zulfan Zidni Ilhama** [LinkedIn](https://www.linkedin.com/in/zulfanzidni/)")
        st.write("Supervised by: **Retno Aulia Vinarti, M.Kom., Ph.D.** [Email](ra_vinarti@its.ac.id)")
        st.write("Expert: **dr. Reza Fahlevi, Sp.A (RSCM UI)**")

    patient_name = st.text_input("Patient Name")
    patient_id = st.text_input("Patient ID")
    date = datetime.now().strftime("%d-%m-%Y")

    # Define variables and their upper limits with labels
    variables = {
        "sex": {"label": "Sex", "default": "Male", "tag": "Sex"},
        "age": {"label": "Age (years)", "default": 5.7, "tag": "Age (Significant)"},
        "weight": {"label": "Weight (kg)", "default": 16.08, "tag": "Weight (Significant)"},
        "prism_score": {"label": "PRISM III Score *", "default": 14.02, "tag": "PRISM III Score (Significant)"},
        "vis": {"label": "Vasoactive-Inotropic Score *", "default": 9.36, "tag": "Vasoactive-Inotropic Score (Significant)"},
        "picu_stay": {"label": "PICU Stay (days)", "default": 13.5, "tag": "PICU Stay"},
        "ventilator": {"label": "Ventilator Usage *", "default": "No", "tag": "Ventilator Usage (Significant)"},
        "admss": {"label": "Interval from Admission (hours)", "default": 18.17, "tag": "Interval from Admission"},
        "crrt": {"label": "Duration of CRRT (days)", "default": 4.23, "tag": "Duration of CRRT (Significant)"},
        "fo": {"label": "Fluid Overload *", "default": "No", "tag": "Fluid Overload (Significant)"},
        "fo_at_crrt": {"label": "% FO at CRRT Initiation *", "default": 8.12, "tag": "% FO at CRRT Initiation (Significant)"},
        "ph": {"label": "pH Level *", "default": 7.33, "tag": "pH Level (Significant)"},
        "lactic": {"label": "Lactic Acid (mmol/L) *", "default": 2.24, "tag": "Lactic Acid"},
        "hb": {"label": "Hemoglobin (g/dL)", "default": 9.45, "tag": "Hemoglobin"},
        "platelet": {"label": "Platelet (103/µL)", "default": 109.54, "tag": "Platelet"},
        "urine_v": {"label": "Urine Volume (mL/Kg/h) *", "default": 0.9, "tag": "Urine Volume"},
        "sepsis": {"label": "Sepsis", "default": "No", "tag": "Sepsis (Significant)"},
        "alf": {"label": "Acute Liver Failure", "default": "No", "tag": "Acute Liver Failure (Significant)"},
        "rsd": {"label": "Respiratory System Disease *", "default": "No", "tag": "Respiratory System Disease (Significant)"},
        "albumin": {"label": "Albumin (g/dL) *", "default": 3.05, "tag": "Albumin (Significant)"},
        "kreatinin": {"label": "Creatinine (mg/dL)", "default": 1.5, "tag": "Creatinine (Significant)"},
        "pelod": {"label": "PELOD Score *", "default": 12.22, "tag": "PELOD Score (Significant)"},
        "psofa": {"label": "pSOFA Score *", "default": 9.56, "tag": "pSOFA Score (Significant)"},
        "bicarbonate": {"label": "Bicarbonate (mmEq/L)", "default": 21.7, "tag": "Bicarbonate"},
        "sodium": {"label": "Sodium (mmol/L)", "default": 138.72, "tag": "Sodium (Significant)"},
        "potassium": {"label": "Potassium (mmol/L)", "default": 3.61, "tag": "Potassium"},
        "tls": {"label": "Tumor Lysis Syndrome", "default": "Yes", "tag": "Tumor Lysis Syndrome"},
        "hyperammonemia": {"label": "Hyperammonemia", "default": "Yes", "tag": "Hyperammonemia"}
    }

    # Define correct categorical options
    categorical_options = {
        "sex": ["Male", "Female"],
        "ventilator": ["Yes", "No"],
        "fo": ["Yes", "No"],
        "sepsis": ["Yes", "No"],
        "alf": ["Yes", "No"],
        "rsd": ["Yes", "No"],
        "tls": ["Yes", "No"],
        "hyperammonemia": ["Yes", "No"]
    }

    # Mark significant variables
    significant_variables = ["age", "weight", "prism_score", "vis", "ventilator", "crrt", "fo", "fo_at_crrt", "ph", "sepsis", "alf", "rsd", "albumin", "kreatinin", "pelod", "psofa", "sodium"]

    # Variables that are correct if higher or same than upper limits
    higher_or_equal_variables = ["ph", "platelet", "urine_v", "albumin", "bicarbonate", "potassium"]

    # Split view into two columns
    col1, col2 = st.columns(2)

    # Input fields for user data
    user_data = {}
    with col1:
        for i, (var, props) in enumerate(variables.items()):
            if i % 2 == 0:  # Variables for column 1
                if var in categorical_options:
                    user_data[var] = st.selectbox(f"{props['label']}", categorical_options[var], index=None)
                else:
                    user_data[var] = st.number_input(f"{props['label']}",step=0.1, value=None, format="%.2f")
    with col2:
        for i, (var, props) in enumerate(variables.items()):
            if i % 2 != 0:  # Variables for column 2
                if var in categorical_options:
                    user_data[var] = st.selectbox(f"{props['label']}", categorical_options[var], index=None)
                else:
                    user_data[var] = st.number_input(f"{props['label']}",step=0.1, value=None, format="%.2f")

    # Calculate score
    if st.button("Calculate"):
        total_variables = 0
        within_limit = 0
        within_limit_vars = []

        for var, props in variables.items():
            value = user_data[var]
            upper_limit = props['default']
            if value is not None:  # Exclude variables with None values
                if var in categorical_options:
                    total_variables += 1
                    if var in significant_variables:
                        total_variables += 1  # Count significant variables twice
                    if value == upper_limit:  # Check if categorical value matches the correct option
                        within_limit += 1
                        within_limit_vars.append(props['tag'])
                        if var in significant_variables:
                            within_limit += 1  # Count significant variables twice
                            # within_limit_vars.append(f"(Significant) {props['tag']}")
                else:
                    total_variables += 1
                    if var in significant_variables:
                        total_variables += 1  # Count significant variables twice
                    if var in higher_or_equal_variables:
                        if value >= upper_limit:
                            within_limit += 1
                            within_limit_vars.append(props['tag'])
                            if var in significant_variables:
                                within_limit += 1
                                # within_limit_vars.append(f"(Significant) {props['tag']}")
                    else:
                        if value <= upper_limit:
                            within_limit += 1
                            within_limit_vars.append(props['tag'])
                            if var in significant_variables:
                                within_limit += 1
                                # within_limit_vars.append(f"(Significant) {props['tag']}")

        if total_variables > 0:
            final_score = (within_limit / total_variables) * 100
            new_row = pd.DataFrame([{"name": patient_name, "id": patient_id, "date": date, **user_data, "survival probability": final_score}])
            df = pd.concat([df, new_row], axis=0, ignore_index=True)

            if final_score >= 50:
                st.success(f"The survival probability score is: {final_score:.2f}%")
            else:
                st.error(f"The survival probability score is: {final_score:.2f}%")
            st.info(f"Variables within the survivor criteria: ({', '.join(within_limit_vars)})")
            st.cache_data.clear()
            # st.info(f"Variables within limit: {', '.join(within_limit_vars)}")
            # st.info(f"Total variables considered: {total_variables}")
        else:
            st.warning("No variables included in the calculation.")
    with st.sidebar:
        st.subheader("Data Pasien (Updated)") 
        
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            "Download Updated Data (as CSV)", 
            data=csv, 
            file_name="crrt_prediction_data_export.csv", 
            mime="text/csv", 
            use_container_width=True, 
            icon=":material/download:",
            key="download_button"
        )
        st.info("Data terbaru diunduh sebagai file CSV.")
#         st.write("Data: [Google Sheets](https://docs.google.com/spreadsheets/d/1uXXWkXhlpDopuzniS-EpY2ukjAogKY-PMobBJFnpQZc/edit?usp=sharing)")
#         if st.download_button("Download Updated Data", data=df.to_csv(), file_name="data_crrt.csv", mime="text/csv", use_container_width=True, icon=":material/download:"):
#             st.cache_data.clear()
#             st.info("Data downloaded successfully.")
# def remove_step_number_input():
#     st.markdown("""
#                 <style>
#                     .css-qn8ina {display: none;}
#                 </style>""",
#                 unsafe_allow_html=True)

if __name__ == "__main__":
    main()