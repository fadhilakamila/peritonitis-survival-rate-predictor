"""
TA | Peritonitis Prediction Calculator
"""
import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(
    page_title="Peritonitis Prediction Calculator",
    page_icon="🔬",
    layout="wide"
)

# === KNOWLEDGE BASE (sesuai decision table) ===
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
    st.title("Sistem Prediksi Survival Rate Pasien Peritoneal Dialysis")
    st.markdown("---")

    with st.sidebar:
        st.header("Informasi Pengembang")
        st.write("Developed by: **Fadhila Kamila Ismail** [LinkedIn](https://www.linkedin.com/in/fadhila-kamila-ismail/)")
        st.write("Supervised by: **Retno Aulia Vinarti, M.Kom., Ph.D.** [Email](ra_vinarti@its.ac.id)")
        st.write("Expert: **dr. Reza Fahlevi, Sp.A(K)**")
        st.info("Sistem ini menggunakan meta-analisis sebagai knowledge-base klinis.")

    st.subheader("Kondisi Klinis Pasien")
    patient_name = st.text_input("Nama Pasien", placeholder="Masukkan nama...")
    
    col1, col2 = st.columns(2)
    user_selections = {}

    for i, var in enumerate(variables_data):
        target_col = col1 if i < 9 else col2
        label = f"{i+1}. {var['label']}"
        options = [var['non-peritonitis'], var['peritonitis']]
        
        choice = target_col.selectbox(label, options, index=0)
        user_selections[var['label']] = choice

    if st.button("Hitung Prediksi Survival Rate"):
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

        st.markdown("---")
        st.subheader(f"Hasil Prediksi **{patient_name}**")
        
        if survival_rate >= 50:
            st.success(f"**SURVIVOR** dengan Survival Rate **{survival_rate:.2f}%**")
            st.caption(f"Pasien dikategorikan sebagai **SURVIVOR** karena Survival Rate ≥ 50% (Cut-off dr. Reza Fahlevi, Sp.A(K))")
        else:
            st.error(f"**NON-SURVIVOR** dengan Survival Rate{survival_rate:.2f}%**")
            st.caption(f"Pasien dikategorikan sebagai **NON-SURVIVOR** karena Survival Rate < 50% (Cut-off dr. Reza Fahlevi, Sp.A(K))")

        # === XAI ===
        expl_col1, expl_col2 = st.columns(2)
        
        with expl_col1:
            st.write("**Mendukung Survival (RR < 1)**")
            for item in xai_supporting_non_peritonitis:
                st.write(f"- {item}")
        
        with expl_col2:
            st.write("⚠️ **Meningkatkan Risiko Peritonitis (RR > 1)**")
            for item in xai_supporting_peritonitis:
                st.write(f"- {item}")

        # Penjelasan MRF 
        if modifiable_risk_factors:
            st.warning("**Modifiable Risk Factor**")
            st.caption("Variabel berikut dapat diperbaiki secara medis untuk meningkatkan peluang keberhasilan terapi")
            
            for mrf in modifiable_risk_factors:
                penjelasan = mrf_explanations.get(mrf,"Perlu konsultasi lebih lanjut dengan dokter spesialis.")

                st.write(f"- {mrf}")
                st.info(penjelasan)

if __name__ == "__main__":
    main()