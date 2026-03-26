import streamlit as st
import os  # Esta librería permite abrir archivos en Windows

st.set_page_config(page_title="App Menú", layout="wide")

# Estilo de los botones
st.markdown("""
    <style>
    .stButton > button {
        width: 100%; height: 100px; font-size: 24px !important;
        font-weight: bold !important; border-radius: 15px;
        margin-bottom: 15px; background-color: #1E293B;
        color: white; border: 2px solid #3B82F6;
    }
    .titulo { text-align: center; font-size: 40px; font-weight: 900; color: #3B82F6; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">MENÚ DE GESTIÓN</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # --- BOTÓN 1: ABRIR EXCEL ---
    if st.button("📄 PLANTILLA (EXCEL)"):
        try:
            # Revisa que el nombre coincida exactamente con tu archivo
            os.startfile("tu_archivo.xlsx") 
            st.success("Abriendo Excel...")
        except Exception as e:
            st.error(f"No se encuentra el archivo: tu_archivo.xlsx")

    if st.button("👤 TUS DATOS"): st.write("Sección Tus Datos")
    if st.button("➕ OTRO"): st.write("Sección Otro")

with col2:
    if st.button("📊 REVISIÓN"): st.write("Cargando Revisión...")
    if st.button("🚀 UNO MÁS"): st.write("Sección Uno Más")
    if st.button("🏁 EL ÚLTIMO"): st.write("Sección El Último")
