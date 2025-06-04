import streamlit as st
import pandas as pd
from pycaret.classification import load_model, predict_model
import base64

# Imagen de fondo
def set_bg_local(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)),
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_local("Campo drone.jpg")

# Estilo barra superior
st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        background-color: #262730;
    }
    [data-testid="stSidebar"] {
        background-color: #262730;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* Track (barra del slider) */
    .stSlider > div[data-baseweb="slider"] > div > div:nth-child(1) {
        background: #2e7d32 !important;
    }
    /* Handle (circulito del slider) */
    .stSlider > div[data-baseweb="slider"] > div > div:nth-child(2) {
        background: #2e7d32 !important;
        border: none !important;
    }
    /* Línea completa de fondo */
    .stSlider > div[data-baseweb="slider"] > div > div:nth-child(3) {
        background: rgba(255,255,255,0.1) !important;
    }
    /* Valor del slider */
    .stSlider label {
        color: white !important;
    }
     /* Botón */
    .stButton > button {
        background-color: #2e7d32 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6em 1.2em !important;
        font-weight: bold !important;
        transition: background-color 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #1b5e20 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Cargar modelo y diccionario
model = load_model("modelo_recomendacion_cultivo")
cultivo_dict = {
    'Barley': 'Cebada', 'Bean': 'Poroto', 'Dagussa': 'Mijo etíope', 'Fallow': 'Barbecho',
    'Maize': 'Maíz', 'Niger seed': 'Semilla de niger', 'Pea': 'Arveja', 'Potato': 'Papa',
    'Red Pepper': 'Ají rojo', 'Sorghum': 'Sorgo', 'Teff': 'Teff', 'Wheat': 'Trigo'
}

# Título principal con espaciado
st.markdown("<br><h1 style='text-align: center; color: white;'> Recomendación de cultivo</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Completá los datos del suelo y clima para obtener el cultivo más adecuado.</p>", unsafe_allow_html=True)

# Agrupar secciones
st.subheader("🔬 Datos del suelo")
ph = st.slider("pH del suelo (escala 0–14)", 3.0, 9.0, 6.5)
k = st.number_input("Potasio – mg/kg", min_value=0, value=100)
p = st.number_input("Fósforo – mg/kg", min_value=0, value=30)
n = st.number_input("Nitrógeno – mg/kg", min_value=0, value=50)
zn = st.number_input("Zinc – mg/kg", min_value=0.0, value=1.0)
s = st.number_input("Azufre – mg/kg", min_value=0.0, value=10.0)
soilcolor = st.selectbox("Color del suelo", [
    'Soilcolor_Dark brown', 'Soilcolor_Reddish brown', 'Soilcolor_dark gray', 'Soilcolor_brown'
])

st.subheader("🌤️ Datos climáticos")
qv2m_w = st.slider("Humedad relativa en invierno – proporción", 0.0, 1.0, 0.5)
t2m_max_sp = st.slider("Temperatura máxima en primavera (°C)", 10.0, 45.0, 28.0)

# Botón centrado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Obtener recomendación de cultivo"):
        input_data = pd.DataFrame({
            'Ph': [ph], 'K': [k], 'P': [p], 'N': [n], 'Zn': [zn], 'S': [s],
            'QV2M-W': [qv2m_w], 'T2M_MAX-Sp': [t2m_max_sp], soilcolor: [1]
        })

        expected_cols = [col for col in model.feature_names_in_ if col != 'label']
        for col in expected_cols:
            if col not in input_data.columns:
                input_data[col] = 0
        input_data = input_data[expected_cols]

        prediction = predict_model(model, data=input_data)
        pred_label = prediction['prediction_label'][0]
        pred_score = prediction['prediction_score'][0]
        cultivo_es = cultivo_dict.get(pred_label, pred_label)

        # Resultado visual
        st.markdown(f"""
        <div style="background-color:  #2e7d32; padding: 1rem; border-radius: 10px; text-align: center;">
            <h3>🌾 Cultivo recomendado: <b>{cultivo_es}</b></h3>
            <p>✅ Confianza del modelo: <b>{pred_score:.0%}</b></p>
        </div>
        """, unsafe_allow_html=True)

# Pie con LinkedIn
st.markdown("""
<hr style="margin-top: 2rem;">
<div style="text-align: center; font-size: 12px; color: gray;">
Desarrollado por <b>Melisa Cardozo</b> – 2025 · <a href='https://www.linkedin.com/in/melisacardozo' target='_blank'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)


