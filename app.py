import streamlit as st
import pandas as pd
from pycaret.classification import load_model, predict_model
import base64  # necesario para codificar la imagen

# 🌄 Función para establecer imagen de fondo local con filtro oscuro
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

# 🔁 Fondo con imagen local
set_bg_local("Campo drone.jpg")

# 🎨 Estilo para la barra superior y sidebar
st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        background-color: #262730;
    }
    [data-testid="stSidebar"] {
        background-color: #262730;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 📦 Cargar modelo
model = load_model("modelo_recomendacion_cultivo")

# 🌾 Diccionario de traducción
cultivo_dict = {
    'Barley': 'Cebada',
    'Bean': 'Poroto',
    'Dagussa': 'Mijo etíope',
    'Fallow': 'Barbecho',
    'Maize': 'Maíz',
    'Niger seed': 'Semilla de niger',
    'Pea': 'Arveja',
    'Potato': 'Papa',
    'Red Pepper': 'Ají rojo',
    'Sorghum': 'Sorgo',
    'Teff': 'Teff',
    'Wheat': 'Trigo'
}

# 🧾 Formulario
st.title("Recomendación de cultivo")
st.write("Completá los datos del suelo y clima para obtener el cultivo más adecuado.")

ph = st.slider("pH del suelo", 3.0, 9.0, 6.5)
k = st.number_input("Potasio (K)", min_value=0, value=100)
p = st.number_input("Fósforo (P)", min_value=0, value=30)
n = st.number_input("Nitrógeno (N)", min_value=0, value=50)
zn = st.number_input("Zinc (Zn)", min_value=0.0, value=1.0)
s = st.number_input("Azufre (S)", min_value=0.0, value=10.0)
qv2m_w = st.slider("Humedad relativa invierno (QV2M-W)", 0.0, 1.0, 0.5)
t2m_max_sp = st.slider("Temp. máx. primavera (T2M_MAX-Sp)", 10.0, 45.0, 28.0)
soilcolor = st.selectbox("Color del suelo", [
    'Soilcolor_Dark brown', 'Soilcolor_Reddish brown', 'Soilcolor_dark gray', 'Soilcolor_brown'
])

# 🔍 Predicción
if st.button("🔍 Predecir cultivo recomendado"):
    # 🧪 Crear input_data y completar columnas
    input_data = pd.DataFrame({
        'Ph': [ph],
        'K': [k],
        'P': [p],
        'N': [n],
        'Zn': [zn],
        'S': [s],
        'QV2M-W': [qv2m_w],
        'T2M_MAX-Sp': [t2m_max_sp],
        soilcolor: [1]
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

    # 🎯 Resultado en tarjeta
    st.markdown(f"""
    <div style="padding: 1rem; border-radius: 10px; background-color: #1e1e1e; color: white; font-size: 18px; text-align: center;">
    🌾 <b>Cultivo recomendado:</b> {cultivo_es} <br> 
    ✅ <b>Confianza:</b> {pred_score:.0%}
    </div>
    """, unsafe_allow_html=True)

    # 🔁 Botón de reinicio
    st.markdown("---")
    if st.button("🔁 Nueva consulta"):
        st.experimental_rerun()

# 🖋 Pie de página
st.markdown("""
<hr style="margin-top: 2rem;">
<div style="text-align: center; font-size: 12px; color: gray;">
 <b>Melisa Cardozo</b> • 2025
</div>
""", unsafe_allow_html=True)
