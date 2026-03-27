import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Gestor Convenio 26-29 Pro", layout="centered")

# Estilo de Alto Contraste Mejorado
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; }
    .titulo { text-align: center; color: #ffffff; font-size: 26px; font-weight: 800; margin-bottom: 20px; text-transform: uppercase; }
    label, .stMarkdown, p, [data-testid="stWidgetLabel"] { color: #ffffff !important; font-weight: 800 !important; font-size: 15px !important; }
    div[data-testid="stMarkdownContainer"] p { color: #ffffff !important; }
    .card-anio { background: #1e293b; border: 1px solid #475569; border-radius: 14px; padding: 18px; margin-bottom: 20px; }
    .val-new { color: #ffffff; font-size: 19px; font-weight: 800; display: block; }
    .pago-mano { background: rgba(245, 158, 11, 0.2); border: 2px dashed #f59e0b; color: #fbbf24; padding: 12px; border-radius: 10px; margin-top: 15px; text-align: center; font-weight: 800; }
    .stButton>button { width: 100%; background-color: #2563eb !important; color: white !important; font-weight: bold !important; border-radius: 10px; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS MAESTROS ---
TRAMOS_BASE = {
    "Cajer@/Reponedor": [18800, 19800, 21000],
    "Asistent@ / Oficial": [21000, 22000, 23000],
    "Adjunt@": [25000, 27000, 29000],
    "Gt": [29500, 31000, 33600, 35000, 38200]
}
MESES = ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

if 'seccion' not in st.session_state: st.session_state.seccion = 'menu'
if 'nombre' not in st.session_state: st.session_state.nombre = ""

# --- MOTOR DE CÁLCULO ---
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
    st.markdown('<p class="titulo">📱 GESTIÓN CONVENIO 26-29</p>', unsafe_allow_html=True)
    st.session_state.nombre = st.text_input("Introduce tu nombre para el informe:", value=st.session_state.nombre)
    if st.session_state.nombre:
        if st.button("📈 SUBIDA SALARIAL"): st.session_state.seccion = 'subida'; st.rerun()
        if st.button("💸 CÁLCULO DE ATRASOS"): st.session_state.seccion = 'atrasos'; st.rerun()
        if st.button("🚪 SALIR"): st.session_state.seccion = 'salir'; st.rerun()

elif st.session_state.seccion == 'atrasos':
    st.markdown(f'<p class="titulo">💸 ATRASOS: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): st.session_state.seccion = 'menu'; st.rerun()
    with st.expander("⚙️ DATOS ATRASOS", expanded=True):
        p_ant_atr = st.number_input("Precio Hora ANTIGUO (€)", value=10.00, format="%.2f")
        h_sem_atr = st.number_input("Cómputo Semanal ACTUAL", value=40.0)
        cat_atr = st.selectbox("Categoría Original", list(TRAMOS_BASE.keys()))
        cambio = st.radio("¿Hubo cambio de categoría?", ["No", "Si"], horizontal=True)
        if cambio == "Si":
            mes_c = st.selectbox("Mes cambio:", MESES); cat_n = st.selectbox("Nueva Categoría:", list(TRAMOS_BASE.keys()))
        mes_h = st.selectbox("Calcular hasta:", MESES)
    
    if st.button("🚀 CALCULAR ATRASOS"):
        h_mens = (h_sem_atr * 44.2) / 12
        idx_h = MESES.index(mes_h) + 1
        p_n = motor_2026(p_ant_atr, h_sem_atr, cat_atr if cambio == "No" else (cat_n if MESES.index(mes_h) >= MESES.index(mes_c) else cat_atr))
        total = (p_n - p_ant_atr) * h_mens * idx_h
        st.markdown(f'<div class="card-anio"><span class="val-new">TOTAL ATRASOS: {total:,.2f} €</span></div>', unsafe_allow_html=True)
        txt = f"INFORME DE ATRASOS - {st.session_state.nombre}\n\nCategoría: {cat_atr}\nPrecio Antiguo: {p_ant_atr}€\nPrecio Nuevo: {p_n:.2f}€\nTotal Atrasos: {total:,.2f}€"
        st.download_button("💾 DESCARGAR ATRASOS", txt, file_name="atrasos.txt")

elif st.session_state.seccion == 'subida':
    st.markdown(f'<p class="titulo">📈 PROYECCIÓN: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): st.session_state.seccion = 'menu'; st.rerun()
    with st.expander("⚙️ CONFIGURACIÓN PROYECCIÓN", expanded=True):
        p_act = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
        h_ant_c = st.number_input("Cómputo Semanal ACTUAL", value=40.0)
        h_new_c = st.number_input("Cómputo Semanal PRÓXIMO", value=40.0)
        pagas = st.selectbox("Número de Pagas", [12, 14])
        cat = st.selectbox("Categoría Profesional", list(TRAMOS_BASE.keys()))
        vista = st.selectbox("Proyectar hasta:", ["2026", "2027", "2028", "2029", "COMPLETO"])

    if st.button("🚀 CALCULAR PROYECCIÓN"):
        h_an_ant, h_an_new = h_ant_c * 44.2, h_new_c * 44.2
        f_j = h_new_c / 40
        limite = 2029 if vista == "COMPLETO" else int(vista)
        p_acum = p_act; informe = f"INFORME SALARIAL PRO - {st.session_state.nombre}\n{'='*40}\n"

        for anio in range(2026, limite + 1):
            fijo, mano_pct = (1.04, 0.02) if anio == 2026 else (1.03, 0.015)
            h_ref = h_an_ant if anio == 2026 else h_an_new
            a_prev = p_acum * h_ref
            
            tramos_anio = TRAMOS_BASE[cat].copy()
            tramos_anio[-1] *= (1.03 ** (anio - 2026))
            sal_fijo = (p_acum * h_an_new) * fijo
            p_u = 0.0
            
            if sal_fijo >= (tramos_anio[-1] * f_j - 0.01):
                n_anual, p_u = sal_fijo, a_prev * mano_pct
            else:
                n_anual = sal_fijo
                for t in tramos_anio:
                    if sal_fijo < t * f_j: n_anual = t * f_j; break
            
            p_nuevo_h = n_anual / h_an_new
            inc = ((p_nuevo_h / p_acum) - 1) * 100
            
            res_txt = f"AÑO {anio}:\n- Precio Hora: {p_nuevo_h:.2f}€ (Inc: {inc:.2f}%)\n- Bruto Anual: {n_anual:,.2f}€\n- Pago Mano Alzada: {p_u:,.2f}€\n{'-'*20}\n"
            informe += res_txt
            p_acum = p_nuevo_h
            
            st.markdown(f'<div class="card-anio"><b>AÑO {anio}</b><br>Precio: {p_nuevo_h:.2f}€/h<br>Anual: {n_anual:,.2f}€<br>Mano Alzada: {p_u:,.2f}€</div>', unsafe_allow_html=True)

        st.download_button("💾 DESCARGAR INFORME COMPLETO", informe, file_name="informe_salarial.txt")

elif st.session_state.seccion == 'salir':
    st.markdown('<p class="titulo">SESIÓN FINALIZADA</p>', unsafe_allow_html=True)
    if st.button("↩️ VOLVER"): st.session_state.seccion = 'menu'; st.rerun()
