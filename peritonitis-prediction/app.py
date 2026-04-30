"""
TA | Peritonitis Prediction Calculator
"""
import streamlit as st
import pandas as pd
import hmac
from datetime import datetime
import os
import streamlit_shadcn_ui as ui

# === PASSWORD ===
def check_password():
    def password_entered():
        if st.session_state["username"] in st.secrets["password"] and hmac.compare_digest(
            st.session_state["password"], st.secrets["password"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.markdown("<h1 style='text-align: center;'>Sistem Prediksi Pediatri</h1>", unsafe_allow_html=True)
    left_co, cent_co, last_co = st.columns([1, 2, 1])
    
    with cent_co:
        st.subheader("Login")
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Login", on_click=password_entered, use_container_width=True)

        if "password_correct" in st.session_state:
            st.error("😕 Username atau password salah.")
            
    return False

# Konfigurasi Halaman
st.set_page_config(
    page_title="Pediatric Prediction System",
    page_icon="🔬",
    layout="wide"
)

if not check_password():
    st.stop()

# # === simpan log ke excel ===
# def save_prediction_log(data_row, module_name):
#     log_file = "prediction_logs.xlsx"
#     data_row['Module'] = module_name
#     data_row['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     new_df = pd.DataFrame([data_row])
    
#     if os.path.exists(log_file):
#         existing_df = pd.read_excel(log_file)
#         updated_df = pd.concat([existing_df, new_df], ignore_index=True)
#     else:
#         updated_df = new_df
        
#     updated_df.to_excel(log_file, index=False)

# # === data loading ===
# @st.cache_data
# def load_crrt_database():
#     file_path = 'PredictCRRTforKids_Database.xlsx'
#     try:
#         return pd.read_excel(file_path)
#     except:
#         return pd.DataFrame()
    
# === nav side bar ===
selection = st.sidebar.radio("Pilih Modul Prediksi", ["Peritonitis Prediction", "CRRT Prediction"])

# === PERITONITIS PREDICTION ===
if selection == "Peritonitis Prediction":
    # --- KNOWLEDGE BASE (sesuai decision table) ---
    # x=1 jika mendukung Non-Survivor (Peritonitis), x=0 jika mendukung Survivor.
    variables_data = [
        {"label": "Age", "non-peritonitis": ">2 yo", "peritonitis": "<2 yo", "p_val": 0.002, "rr": 1.4, "mrf": False},
        {"label": "Gender", "non-peritonitis": "Female", "peritonitis": "Male", "p_val": 0.09, "rr": 1.08, "mrf": False},
        {"label": "Duration of PD", "non-peritonitis": "<12 mo", "peritonitis": ">12 mo", "p_val": 0.001, "rr": 2.29, "mrf": False},
        {"label": "Place of Residence", "non-peritonitis": "Rural", "peritonitis": "Urban", "p_val": 0.08, "rr": 1.22, "mrf": False},
        {"label": "Housing", "non-peritonitis": "Good service", "peritonitis": "Fair/poor service", "p_val": 0.77, "rr": 0.92, "mrf": True},
        {"label": "Socioeconomic", "non-peritonitis": "Good", "peritonitis": "Poor/fair", "p_val": 0.09, "rr": 0.84, "mrf": True},
        {"label": "Education", "non-peritonitis": "Studies", "peritonitis": "Illiterate", "p_val": 0.48, "rr": 1.21, "mrf": False},
        {"label": "Peritonitis in ESI", "non-peritonitis": "No ESI", "peritonitis": "ESI", "p_val": 0.0001, "rr": 1.35, "mrf": True},
        {"label": "Nutrition", "non-peritonitis": "Normal Nutrition", "peritonitis": "Poor nutrition", "p_val": 0.19, "rr": 0.89, "mrf": True},
        {"label": "Cause of ESRD", "non-peritonitis": "Glomerular", "peritonitis": "Non-glomerular", "p_val": 0.04, "rr": 1.13, "mrf": False},
        {"label": "Type of Catheter (Shape)", "non-peritonitis": "Coiled/swan neck", "peritonitis": "Straight", "p_val": 0.48, "rr": 1.15, "mrf": True},
        {"label": "Type of Catheter (Cuff)", "non-peritonitis": "Double", "peritonitis": "Single cuff", "p_val": 0.32, "rr": 1.33, "mrf": True},
        {"label": "Catheter Placement", "non-peritonitis": "Open", "peritonitis": "Laparoscopic", "p_val": 0.85, "rr": 1.03, "mrf": True},
        {"label": "Gastrostomy/Intraperitoneal Device", "non-peritonitis": "No", "peritonitis": "Yes", "p_val": 0.23, "rr": 0.78, "mrf": True},
        {"label": "Performed CAPD", "non-peritonitis": "Patients", "peritonitis": "Parents/others", "p_val": 0.27, "rr": 0.81, "mrf": True},
        {"label": "Starting PD <2 weeks after placement", "non-peritonitis": "No", "peritonitis": "Yes", "p_val": 0.23, "rr": 1.37, "mrf": True},
        {"label": "Catheter Orientation", "non-peritonitis": "Lateral/downward", "peritonitis": "upward", "p_val": 0.12, "rr": 0.66, "mrf": True},
        {"label": "Stunting", "non-peritonitis": "No stunting", "peritonitis": "Stunting", "p_val": 0.32, "rr": 0.72, "mrf": True},
    ]

    mrf_explanations = {
        "Housing": "Perlu perbaikan sanitasi dan fasilitas lingkungan tempat tinggal untuk mengurangi risiko kontaminasi kuman dari lingkungan.",
        "Nutrition": "Perlu peningkatan asupan nutrisi dan pemantauan status gizi secara berkala oleh ahli gizi anak untuk mencapai status gizi normal.",
        "Socioeconomic": "Perlu dukungan biaya kesehatan atau bantuan pekerja sosial untuk memastikan kepatuhan terapi dan ketersediaan logistik dialisis.",
        "Performed CAPD": "Perlu pelatihan ulang yang intensif bagi orang yang melakukan dialisis (pasien/keluarga) mengenai prosedur aseptik yang benar.",
        "Gastronomy Device": "Perlu perawatan ekstra dan pembersihan ketat pada area lubang alat tambahan di perut untuk mencegah infeksi silang ke area kateter.",
        "Stunting": "Perlu optimalisasi pertumbuhan melalui dukungan nutrisi agresif atau terapi hormon pertumbuhan sesuai saran dokter.",
        "Starting PD <2 weeks after placement": "Sebaiknya menunda dimulainya dialisis (jika kondisi klinis memungkinkan) minimal 2 minggu setelah operasi agar luka kateter sembuh sempurna.",
        "Peritonitis in ESI": "Perlu penanganan agresif dan segera terhadap infeksi area keluar kateter (Exit Site Infection) agar kuman tidak masuk ke rongga perut.",
        "Type of Catheter (Cuff)": "Disarankan menggunakan kateter dengan 'Double Cuff' karena memberikan perlindungan ganda (barier bakteri) yang lebih baik.",
        "Type of Catheter (Shape)": "Penggunaan kateter berbentuk 'Coiled' atau 'Swan-neck' lebih disarankan untuk mengurangi risiko kateter berpindah posisi (displacement).",
        "Catheter Placement": "Berdasarkan hasil meta-analisis, metode 'Open' pada populasi ini menunjukkan kecenderungan risiko peritonitis yang lebih rendah dibandingkan 'Laparoscopic'. Konsultasikan untuk teknik yang paling sesuai."
    }

    def main():
        st.title("Prediksi Survival Rate Pasien Pediatri Peritoneal Dialysis")

        with st.sidebar:
            st.write("Developed by: **Fadhila Kamila Ismail** [LinkedIn](https://www.linkedin.com/in/fadhila-kamila-ismail/)")
            st.write("Supervised by: **Retno Aulia Vinarti, M.Kom., Ph.D.** [Email](ra_vinarti@its.ac.id)")
            st.write("Expert: **dr. Reza Fahlevi, Sp.A(K)**")
            st.info("Sistem ini menggunakan meta-analisis sebagai knowledge-base klinis.")

        st.subheader("Masukkan Kondisi Klinis Pasien")
        patient_name = st.text_input("Nama Pasien", placeholder="Masukkan nama...")
        
        col1, col2 = st.columns(2)
        user_selections = {}

        for i, var in enumerate(variables_data):
            target_col = col1 if i < 9 else col2
            label = f"{i+1}. {var['label']}"
            options = [var['non-peritonitis'], var['peritonitis']]
            
            choice = target_col.selectbox(label, options, index=0)
            user_selections[var['label']] = choice

        if st.button("Hitung Survival Rate"):
            if not patient_name:
                st.warning("Silakan masukkan nama pasien terlebih dahulu.")
                return

            total_wi_xi = 0
            total_wi = 0
            
            xai_supporting_non_peritonitis = []
            xai_supporting_peritonitis = []
            modifiable_risk_factors = []

            # === PERHITUNGAN WEIGHTED AVERAGE ===
            for var in variables_data:
                # Bobot (wi)
                weight = 2 if var['p_val'] < 0.05 else 1
                
                # Nilai (xi)
                # x=1 jika pilihan user adalah peritonitis, x=0 jika non-peritonitis
                x_val = 1 if user_selections[var['label']] == var['peritonitis'] else 0
                
                total_wi_xi += (weight * x_val)
                total_wi += weight

                # === PERSIAPAN DATA XAI === 
                if x_val == 0:
                    xai_supporting_non_peritonitis.append(var['label'])
                else:
                    xai_supporting_peritonitis.append(var['label'])
                
                # Identifikasi MRF
                if var['mrf'] and x_val == 1:
                    modifiable_risk_factors.append(var['label'])

            # Rumus Kejadian Peritonitis
            kejadian_peritonitis = total_wi_xi / total_wi
            # Rumus Survival Rate (SR)
            survival_rate = (1 - kejadian_peritonitis) * 100

            st.divider()
            st.subheader(f"📊 Laporan Hasil Analisis: {patient_name}")

            # 1. Menampilkan Survival Rate dengan Metric Card (Shadcn)
            # Kita tentukan warna berdasarkan hasil
            result_status = "SURVIVOR" if survival_rate >= 50 else "NON-SURVIVOR"
            result_color = "default" if survival_rate >= 50 else "destructive"

            cols = st.columns([1, 1])
            with cols[0]:
                ui.metric_card(
                    title="Survival Rate", 
                    content=f"{survival_rate:.2f}%", 
                    description=f"Status: {result_status}", 
                    key="sr_metric"
                )

            with cols[1]:
                # Alert Shadcn untuk memberikan kesimpulan cepat
                if survival_rate >= 50:
                    ui.alert(
                        title="Prediksi Positif", 
                        content=f"Pasien dikategorikan sebagai SURVIVOR berdasarkan cut-off 50%.", 
                        variant="default", 
                        icon="check_circle"
                    )
                else:
                    ui.alert(
                        title="Perhatian Medis", 
                        content=f"Pasien dikategorikan sebagai NON-SURVIVOR. Diperlukan pengawasan ketat.", 
                        variant="destructive", 
                        icon="warning"
                    )

            # 2. XAI dengan Card dan Badges (Shadcn)
            st.markdown("### 🔍 Penjelasan Faktor (XAI)")
            expl_col1, expl_col2 = st.columns(2)

            with expl_col1:
                with ui.card(title="Faktor Pendukung Survival", description="Variabel dengan Risk Ratio (RR) < 1"):
                    if xai_supporting_non_peritonitis:
                        # Menampilkan list menggunakan badges agar terlihat modern
                        badges = [(item, "outline") for item in xai_supporting_non_peritonitis]
                        ui.badges(badge_list=badges, class_name="flex flex-wrap gap-2")
                    else:
                        st.write("Tidak ada faktor spesifik terdeteksi.")

            with expl_col2:
                with ui.card(title="Faktor Risiko Peritonitis", description="Variabel dengan Risk Ratio (RR) > 1"):
                    if xai_supporting_peritonitis:
                        badges = [(item, "destructive") for item in xai_supporting_peritonitis]
                        ui.badges(badge_list=badges, class_name="flex flex-wrap gap-2")
                    else:
                        st.write("Risiko terpantau rendah.")

            # 3. Modifiable Risk Factor (MRF) dengan Accordion/Card
            if modifiable_risk_factors:
                st.markdown("### 🛠️ Rekomendasi Intervensi (MRF)")
                ui.alert(
                    title="Faktor Risiko yang Dapat Dimodifikasi",
                    content="Berikut adalah langkah medis yang dapat diambil untuk meningkatkan peluang survival.",
                    variant="outline"
                )
                
                # Loop untuk menampilkan setiap MRF dalam Card kecil yang rapi
                for mrf in modifiable_risk_factors:
                    penjelasan = mrf_explanations.get(mrf, "Perlu konsultasi lebih lanjut.")
                    with ui.card(title=f"Rekomendasi: {mrf}"):
                        st.write(penjelasan)

            # st.markdown("---")
            # st.subheader(f"Hasil Prediksi **{patient_name}**")
            
            # if survival_rate >= 50:
            #     st.success(f"**SURVIVOR** dengan Survival Rate **{survival_rate:.2f}%**")
            #     st.caption(f"Pasien dikategorikan sebagai **SURVIVOR** karena Survival Rate ≥ 50%")
            # else:
            #     st.error(f"**NON-SURVIVOR** dengan Survival Rate **{survival_rate:.2f}%**")
            #     st.caption(f"Pasien dikategorikan sebagai **NON-SURVIVOR** karena Survival Rate < 50% (Cut-off dr. Reza Fahlevi, Sp.A(K))")

            # # === XAI ===
            # expl_col1, expl_col2 = st.columns(2)
            
            # st.space()

            # with expl_col1:
            #     st.write("**Mendukung Survival (RR < 1)**")
            #     for item in xai_supporting_non_peritonitis:
            #         st.write(f"- {item}")
            
            # with expl_col2:
            #     st.write("**Meningkatkan Risiko Peritonitis (RR > 1)**")
            #     for item in xai_supporting_peritonitis:
            #         st.write(f"- {item}")

            # st.space()

            # if modifiable_risk_factors:
            #     st.write("**Modifiable Risk Factor**")
            #     st.caption("Variabel berikut dapat diperbaiki secara medis untuk meningkatkan peluang keberhasilan terapi")
                
            #     for mrf in modifiable_risk_factors:
            #         penjelasan = mrf_explanations.get(mrf,"Perlu konsultasi lebih lanjut dengan dokter spesialis.")

            #         st.write(f"- {mrf}")
            #         st.info(penjelasan)

    if __name__ == "__main__":
        main()

elif selection == "CRRT Prediction":
    st.title("Survival Prediction Calculator for Pediatric CRRT")

    with st.sidebar:
        st.write("Developed by: **Zulfan Zidni Ilhama** [LinkedIn](https://www.linkedin.com/in/zulfanzidni/)")
        st.write("Supervised by: **Retno Aulia Vinarti, M.Kom., Ph.D.** [Email](ra_vinarti@its.ac.id)")
        st.write("Expert: **dr. Reza Fahlevi, Sp.A(K)**")
    
    df_crrt = load_crrt_database()

    patient_name = st.text_input("Patient Name")
    patient_id = st.text_input("Patient ID")
    date = datetime.now().strftime("%d-%m-%Y")

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

    if st.button("Calculate"):
        total_variables = 0
        within_limit = 0
        within_limit_vars = []

        for var, props in variables.items():
            value = user_data[var]
            upper_limit = props['default']
            if value is not None:
                if var in categorical_options:
                    total_variables += 1
                    if var in significant_variables:
                        total_variables += 1
                    if value == upper_limit:
                        within_limit += 1
                        within_limit_vars.append(props['tag'])
                        if var in significant_variables:
                            within_limit += 1 
                else:
                    total_variables += 1
                    if var in significant_variables:
                        total_variables += 1  
                    if var in higher_or_equal_variables:
                        if value >= upper_limit:
                            within_limit += 1
                            within_limit_vars.append(props['tag'])
                            if var in significant_variables:
                                within_limit += 1
                    else:
                        if value <= upper_limit:
                            within_limit += 1
                            within_limit_vars.append(props['tag'])
                            if var in significant_variables:
                                within_limit += 1

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
        else:
            st.warning("No variables included in the calculation.")