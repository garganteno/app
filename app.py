import streamlit as st
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="Gestor Convenio 26-29 Pro", layout="centered")

# BLOQUEO TOTAL DE ICONOS Y ESTILO DE ALTO IMPACTO (EL QUE TE GUSTABA)
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], header, footer { display: none !important; visibility: hidden !important; }
    .stApp { background: #0a0f1e; padding-top: 0px !important; }
    .titulo { text-align: center; color: #ffffff; font-size: 26px; font-weight: 800; margin-bottom: 20px; text-transform: uppercase; }
    label { color: #ffffff !important; font-weight: 800 !important; font-size: 15px !important; }
    .card-anio { background: #1e293b; border: 1px solid #475569; border-radius: 14px; padding: 18px; margin-bottom: 20px; }
    .header-anio { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #475569; padding-bottom: 10px; }
    .badge-inc { background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: 700; }
    .grid-datos { display: flex; flex-direction: column; gap: 12px; }
    @media (min-width: 600px) { .grid-datos { flex-direction: row; justify-content: space-between; } .col-dato { flex: 1; } }
    .col-dato { background: #0f172a; padding: 12px; border-radius: 10px; border-left: 4px solid #3b82f6; }
    .label-dato { color: #94a3b8; font-size: 11px; text-transform: uppercase; font-weight: 700; margin-bottom: 4px; }
    .val-old { color: #cbd5e1; font-size: 14px; display: block; margin-bottom: 2px; }
    .val-new { color: #ffffff; font-size: 20px; font-weight: 800; display: block; }
    .pago-mano { background: rgba(245, 158, 11, 0.15); border: 1px dashed #f59e0b; color: #fbbf24; padding: 10px; border-radius: 8px; margin-top: 15px; text-align: center; font-weight: 700; }
    .stButton>button { width: 100%; background-color: #2563eb !important; color: white !important; font-weight: bold !important; height: 50px; border-radius: 10px; margin-bottom: 10px; }
    div[data-testid="stMarkdownContainer"] p { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS MAESTROS ---
TRAMOS_BASE = {"Cajer@/Reponedor": [18800, 19800, 21000], "Asistent@ / Oficial": [21000, 22000, 23000], "Adjunt@": [25000, 27000, 29000], "Gt": [29500, 31000, 33600, 35000, 38200]}
MESES = ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

if 'seccion' not in st.session_state: st.session_state.seccion = 'menu'
if 'nombre' not in st.session_state: st.session_state.nombre = ""

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
    with st.expander("⚙️ DATOS DE HORAS", expanded=True):
        cat_f = st.selectbox("Categoría Profesional", list(TRAMOS_BASE.keys()))
        p_ant_f = st.number_input("Precio Hora ANTIGUO (€)", value=10.00, format="%.2f")
        h_sem_f = st.number_input("Cómputo Semanal ACTUAL", value=40.0)
        h_dom = st.number_input("Total HORAS trabajadas en DOMINGOS", value=0.0)
        h_fes = st.number_input("Total HORAS trabajadas en FESTIVOS", value=0.0)

    if st.button("🚀 CALCULAR ATRASOS DOM/FES"):
        p_new_f = motor_2026(p_ant_f, h_sem_f, cat_f)
        p_h_dom_ant = (50.0 / 8) if "Cajer" in cat_f else (60.0 / 8)
        dif_dom = ((p_new_f * 2) - p_h_dom_ant) * h_dom
        dif_fes = ((p_new_f * 1.5) - (p_ant_f * 1.5)) * h_fes
        total_atraso_f = dif_dom + dif_fes
        st.markdown(f'<div class="card-anio"><p class="label-dato">TOTAL ATRASOS DOM/FES</p><span class="val-new">{total_atraso_f:,.2f} € bruto</span></div>', unsafe_allow_html=True)
        st.download_button("💾 GRABAR (.TXT)", f"Atrasos Dom/Fes {st.session_state.nombre}: {total_atraso_f:.2f}€", file_name="festivos.txt")

elif st.session_state.seccion == 'subida':
    st.markdown(f'<p class="titulo">📈 PROYECCIÓN: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ", key="up"): st.session_state.seccion = 'menu'; st.rerun()
    with st.expander("⚙️ CONFIGURACIÓN", expanded=True):
        p_act = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
        h_ant_i = st.number_input("Cómputo Semanal ACTUAL", value=40.0)
        h_new_i = st.number_input("Cómputo Semanal PRÓXIMO", value=40.0)
        pagas = st.selectbox("Número de Pagas", [12, 14])
        cat = st.selectbox("Categoría Profesional", list(TRAMOS_BASE.keys()))
        vista = st.selectbox("Proyectar hasta:", ["2026", "2027", "2028", "2029", "COMPLETO"])

    if st.button("🚀 CALCULAR PROYECCIÓN"):
        h_an_ant, h_an_new = h_ant_i * 44.2, h_new_i * 44.2
        f_j, p_acum = h_new_i / 40, p_act
        limite = 2029 if vista == "COMPLETO" else int(vista)
        informe_txt = f"MENSUAL ANTIGUO: {(p_act * h_an_ant / pagas):,.2f} € bruto\n"
        for anio in range(2026, limite + 1):
            h_ref = h_an_ant if anio == 2026 else h_an_new
            p_prev = p_acum
            fijo, mano_pct = (1.04, 0.02) if anio == 2026 else (1.03, 0.015)
            tramos_anio = TRAMOS_BASE[cat].copy()
            tramos_anio[-1] *= (1.03 ** (anio - 2026))
            sal_fijo = (p_prev * h_an_new) * fijo
            n_anual, p_u = 0, 0.0
            if sal_fijo >= (tramos_anio[-1] * f_j - 0.01):
                n_anual, p_u = sal_fijo, (p_prev * h_ref) * mano_pct
            else:
                n_anual = sal_fijo
                for t in tramos_anio:
                    if sal_fijo < t * f_j: n_anual = t * f_j; break
            p_acum = n_anual / h_an_new
            st.markdown(f'<div class="card-anio"><b>AÑO {anio}</b><br>Precio: {p_acum:.2f}€/h<br>Mensual: {(n_anual/pagas):,.2f}€ bruto</div>', unsafe_allow_html=True)
            informe_txt += f"AÑO {anio}: {p_acum:.2f}€/h | Mensual: {(n_anual/pagas):,.2f}€ bruto\n"
        st.download_button("💾 GRABAR (.TXT)", informe_txt, file_name="informe.txt")

elif st.session_state.seccion == 'atrasos':
    st.markdown(f'<p class="titulo">💸 ATRASOS: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): st.session_state.seccion = 'menu'; st.rerun()
    with st.expander("⚙️ DATOS ATRASOS", expanded=True):
        p_ant_atr = st.number_input("Precio Hora ANTIGUO (€)", value=10.00, format="%.2f")
        h_sem_atr = st.number_input("Cómputo Semanal ACTUAL", value=40.0)
        cat_atr = st.selectbox("Categoría Original", list(TRAMOS_BASE.keys()))
        mes_h = st.selectbox("Calcular hasta:", MESES)
    if st.button("🚀 CALCULAR ATRASOS"):
        p_n = motor_2026(p_ant_atr, h_sem_atr, cat_atr)
        total = (p_n - p_ant_atr) * ((h_sem_atr * 44.2) / 12) * (MESES.index(mes_h) + 1)
        st.markdown(f'<div class="card-anio"><span class="val-new">TOTAL: {total:,.2f} € bruto</span></div>', unsafe_allow_html=True)

elif st.session_state.seccion == 'salir':
    st.markdown('<p class="titulo">SESIÓN FINALIZADA</p>', unsafe_allow_html=True)
    if st.button("↩️ REINICIAR"): st.session_state.seccion = 'menu'; st.rerun()
