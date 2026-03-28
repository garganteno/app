import streamlit as st
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="Gestor Convenio 26-29 Pro", layout="centered")

# BLOQUEO DE ICONOS Y ESTILO DE ALTO IMPACTO
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], header, footer { display: none !important; visibility: hidden !important; }
    .stApp { background: #0a0f1e; padding-top: 0px !important; }
    .titulo { text-align: center; color: #ffffff; font-size: 26px; font-weight: 800; margin-bottom: 20px; text-transform: uppercase; }
    label { color: #ffffff !important; font-weight: 800 !important; font-size: 15px !important; }
    .card-anio { background: #1e293b; border: 1px solid #475569; border-radius: 14px; padding: 18px; margin-bottom: 20px; }
    .col-dato { background: #0f172a; padding: 12px; border-radius: 10px; border-left: 4px solid #3b82f6; margin-bottom: 10px; }
    .label-dato { color: #94a3b8; font-size: 11px; text-transform: uppercase; font-weight: 700; margin-bottom: 4px; }
    .val-new { color: #ffffff; font-size: 20px; font-weight: 800; display: block; }
    .stButton>button { width: 100%; background-color: #2563eb !important; color: white !important; font-weight: bold !important; height: 50px; border-radius: 10px; margin-bottom: 10px; }
    div[data-testid="stMarkdownContainer"] p { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS MAESTROS ---
TRAMOS_BASE = {"Cajer@/Reponedor": [18800, 19800, 21000], "Asistent@ / Oficial": [21000, 22000, 23000], "Adjunt@": [25000, 27000, 29000], "Gt": [29500, 31000, 33600, 35000, 38200]}
MESES = ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

if 'seccion' not in st.session_state: st.session_state.seccion = 'menu'
if 'nombre' not in st.session_state: st.session_state.nombre = ""

# --- MOTOR DE CÁLCULO 2026 ---
def motor_2026(p_ant, h_sem, cat):
    h_an = h_sem * 44.2
    f_j = h_sem / 40
    sal_proy = (p_ant * h_an) * 1.04
    tramos = TRAMOS_BASE[cat].copy()
    ult_tramo = tramos[-1] * f_j
    if sal_proy >= (ult_tramo - 0.01): return sal_proy / h_an
    for t in tramos:
        t_aj = t * f_j
        if sal_proy < t_aj: return t_aj / h_an
    return sal_proy / h_an

# --- NAVEGACIÓN ---
if st.session_state.seccion == 'menu':
    st.markdown('<p class="titulo">🚀 GESTIÓN CONVENIO 26-29</p>', unsafe_allow_html=True)
    st.session_state.nombre = st.text_input("Introduce tu nombre:", value=st.session_state.nombre)
    if st.session_state.nombre:
        if st.button("📈 SUBIDA SALARIAL"): st.session_state.seccion = 'subida'; st.rerun()
        if st.button("💸 CÁLCULO DE ATRASOS"): st.session_state.seccion = 'atrasos'; st.rerun()
        if st.button("📅 ATRASOS DOMINGOS Y FESTIVOS"): st.session_state.seccion = 'festivos'; st.rerun()
        if st.button("🚪 SALIR"): st.session_state.seccion = 'salir'; st.rerun()

elif st.session_state.seccion == 'festivos':
    st.markdown(f'<p class="titulo">📅 DOMINGOS Y FESTIVOS: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): st.session_state.seccion = 'menu'; st.rerun()
    
    with st.expander("⚙️ DATOS DE HORAS TRABAJADAS", expanded=True):
        cat_f = st.selectbox("Selecciona Categoría", list(TRAMOS_BASE.keys()))
        p_ant_f = st.number_input("Precio Hora ANTIGUO (€)", value=10.00, format="%.2f")
        h_sem_f = st.number_input("Cómputo Semanal ACTUAL", value=40.0)
        h_dom = st.number_input("Total HORAS trabajadas en DOMINGOS", value=0.0, step=0.5)
        h_fes = st.number_input("Total HORAS trabajadas en FESTIVOS", value=0.0, step=0.5)

    if st.button("🚀 CALCULAR ATRASOS FESTIVOS"):
        p_new_f = motor_2026(p_ant_f, h_sem_f, cat_f)
        
        # Domingos: Antes 50/60€ (para 8h) -> Ahora precio hora doble por cada hora
        precio_h_dom_ant = (50.0 / 8) if "Cajer" in cat_f else (60.0 / 8)
        precio_h_dom_new = p_new_f * 2
        dif_dom = (precio_h_dom_new - precio_h_dom_ant) * h_dom
        
        # Festivos: Antes 150% antiguo -> Ahora 150% nuevo
        precio_h_fes_ant = p_ant_f * 1.5
        precio_h_fes_new = p_new_f * 1.5
        dif_fes = (precio_h_fes_new - precio_h_fes_ant) * h_fes
        
        total_bruto = dif_dom + dif_fes
        
        st.markdown(f"""
            <div class="card-anio">
                <div class="col-dato"><p class="label-dato">Atrasos por Horas Domingo</p><span class="val-new">{dif_dom:,.2f} €</span></div>
                <div class="col-dato"><p class="label-dato">Atrasos por Horas Festivo</p><span class="val-new">{dif_fes:,.2f} €</span></div>
                <div style="border-top: 1px solid #475569; padding-top:10px; margin-top:10px; text-align:center;">
                    <p class="label-dato">TOTAL ATRASOS DOM/FES</p>
                    <span style="color:#10b981; font-size:24px; font-weight:900;">{total_bruto:,.2f} € bruto</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        inf_f = f"Atrasos Dom/Fes - {st.session_state.nombre}\nHoras Dom: {h_dom}\nHoras Fes: {h_fes}\nTotal Bruto: {total_bruto:.2f}€"
        st.download_button("💾 GRABAR INFORME (.TXT)", inf_f, file_name=f"festivos_{st.session_state.nombre}.txt")
        if st.button("⬅️ VOLVER AL MENÚ", key="back_fes_bot"): st.session_state.seccion = 'menu'; st.rerun()

elif st.session_state.seccion == 'atrasos':
    st.markdown(f'<p class="titulo">💸 ATRASOS: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ", key="back_atr"): st.session_state.seccion = 'menu'; st.rerun()
    with st.expander("⚙️ CONFIGURACIÓN ATRASOS", expanded=True):
        p_ant_atr = st.number_input("Precio Hora ANTIGUO (€)", value=10.00, format="%.2f")
        h_sem_atr = st.number_input("Cómputo Semanal ACTUAL", value=40.0)
        cat_atr = st.selectbox("Categoría Original", list(TRAMOS_BASE.keys()))
        mes_h = st.selectbox("Calcular hasta:", MESES)
    if st.button("🚀 CALCULAR ATRASOS"):
        h_mens = (h_sem_atr * 44.2) / 12
        p_n = motor_2026(p_ant_atr, h_sem_atr, cat_atr)
        total = (p_n - p_ant_atr) * h_mens * (MESES.index(mes_h) + 1)
        st.markdown(f'<div class="card-anio"><span class="val-new">TOTAL: {total:,.2f} € bruto</span></div>', unsafe_allow_html=True)

elif st.session_state.seccion == 'subida':
    st.markdown(f'<p class="titulo">📈 PROYECCIÓN: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ", key="back_sub"): st.session_state.seccion = 'menu'; st.rerun()
    # (Resto del código de subida salarial que ya tenías impecable)

elif st.session_state.seccion == 'salir':
    st.markdown('<p class="titulo">SESIÓN FINALIZADA</p>', unsafe_allow_html=True)
    if st.button("↩️ REINICIAR"): st.session_state.seccion = 'menu'; st.rerun()
