import streamlit as st
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="Gestor Convenio 26-29 Pro", layout="centered")

# --- BLOQUEO TOTAL POR JAVASCRIPT Y CSS (NIVEL SISTEMA) ---
st.markdown("""
    <script>
    // Función para eliminar elementos de cuenta y sistema de raíz
    function cleanUI() {
        const selectors = [
            'header', 'footer', '#MainMenu', '.stDeployButton', 
            '[data-testid="stToolbar"]', '[data-testid="stDecoration"]',
            '[data-testid="stStatusWidget"]', '#viewerBadge',
            '.viewerBadge_container__1QSob', 'button[title="View source"]'
        ];
        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => el.remove());
        });
    }
    // Ejecutar cada segundo para evitar que vuelvan a aparecer
    setInterval(cleanUI, 1000);
    </script>
    
    <style>
    /* Refuerzo por CSS para ocultar todo */
    [data-testid="stHeader"], [data-testid="stToolbar"], header, footer {
        display: none !important;
        visibility: hidden !important;
    }
    .stApp { background: #0a0f1e; padding-top: 0px !important; }
    .titulo { text-align: center; color: #ffffff; font-size: 26px; font-weight: 800; margin-bottom: 20px; text-transform: uppercase; }
    label { color: #ffffff !important; font-weight: 800 !important; font-size: 15px !important; }
    .card-anio { background: #1e293b; border: 1px solid #475569; border-radius: 14px; padding: 18px; margin-bottom: 20px; }
    .col-dato { background: #0f172a; padding: 12px; border-radius: 10px; border-left: 4px solid #3b82f6; }
    .label-dato { color: #94a3b8; font-size: 11px; text-transform: uppercase; font-weight: 700; margin-bottom: 4px; }
    .val-new { color: #ffffff; font-size: 20px; font-weight: 800; display: block; }
    .pago-mano { background: rgba(245, 158, 11, 0.15); border: 1px dashed #f59e0b; color: #fbbf24; padding: 10px; border-radius: 8px; margin-top: 15px; text-align: center; font-weight: 700; }
    .stButton>button { width: 100%; background-color: #2563eb !important; color: white !important; font-weight: bold !important; height: 50px; border-radius: 10px; }
    div[data-testid="stMarkdownContainer"] p { color: #ffffff !important; }
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
    st.markdown('<p class="titulo">🚀 GESTIÓN CONVENIO 26-29</p>', unsafe_allow_html=True)
    st.session_state.nombre = st.text_input("Introduce tu nombre:", value=st.session_state.nombre)
    if st.session_state.nombre:
        if st.button("📈 SUBIDA SALARIAL"): st.session_state.seccion = 'subida'; st.rerun()
        if st.button("💸 CÁLCULO DE ATRASOS"): st.session_state.seccion = 'atrasos'; st.rerun()
        if st.button("🚪 SALIR"): st.session_state.seccion = 'salir'; st.rerun()

elif st.session_state.seccion == 'subida':
    st.markdown(f'<p class="titulo">📈 PROYECCIÓN: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ", key="up"): st.session_state.seccion = 'menu'; st.rerun()
    
    with st.expander("⚙️ CONFIGURACIÓN", expanded=True):
        p_act = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
        h_ant_i = st.number_input("Cómputo Semanal ACTUAL", value=40.0)
        h_new_i = st.number_input("Cómputo Semanal PRÓXIMO", value=40.0)
        pagas = st.selectbox("Pagas", [12, 14])
        cat = st.selectbox("Categoría Profesional", list(TRAMOS_BASE.keys()))
        vista = st.selectbox("Proyectar hasta:", ["2026", "2027", "2028", "2029", "COMPLETO"])

    if st.button("🚀 CALCULAR"):
        h_an_ant, h_an_new = h_ant_i * 44.2, h_new_i * 44.2
        f_j = h_new_i / 40
        limite = 2029 if vista == "COMPLETO" else int(vista)
        p_acum = p_act
        
        m_ant_real = (p_act * h_an_ant) / pagas
        informe_txt = f"MENSUAL ANTIGUO: {m_ant_real:,.2f} € bruto\n"
        informe_txt += f"INFORME SALARIAL PRO - {st.session_state.nombre.upper()}\n" + "="*40 + "\n"

        for anio in range(2026, limite + 1):
            h_ref = h_an_ant if anio == 2026 else h_an_new
            p_prev = p_acum
            a_prev, m_prev = p_prev * h_ref, (p_prev * h_ref) / pagas
            fijo, mano_pct = (1.04, 0.02) if anio == 2026 else (1.03, 0.015)
            tramos_anio = TRAMOS_BASE[cat].copy()
            tramos_anio[-1] *= (1.03 ** (anio - 2026))
            sal_fijo = (p_prev * h_an_new) * fijo
            n_anual, p_u = 0, 0.0
            
            if sal_fijo >= (tramos_anio[-1] * f_j - 0.01):
                n_anual, p_u = sal_fijo, a_prev * mano_pct
            else:
                n_anual = sal_fijo
                for t in tramos_anio:
                    if sal_fijo < t * f_j: n_anual = t * f_j; break
            
            p_acum = n_anual / h_an_new
            m_new = n_anual / pagas
            
            st.markdown(f"""
                <div class="card-anio">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #475569; padding-bottom: 5px;">
                        <span style="color:white; font-size:18px; font-weight:800;">AÑO {anio}</span>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 10px;">
                        <div class="col-dato"><p class="label-dato">Precio Hora</p><span class="val-new">{p_acum:.2f} €</span></div>
                        <div class="col-dato"><p class="label-dato">Mensual Bruto</p><span class="val-new">{m_new:,.2f} €</span></div>
                    </div>
                    {f'<div class="pago-mano">💰 PAGO MANO ALZADA: {p_u:,.2f} € bruto</div>' if p_u > 0 else ""}
                </div>
            """, unsafe_allow_html=True)
            informe_txt += f"AÑO {anio}: {p_acum:.2f}€/h | Mensual Bruto: {m_new:,.2f}€ | Pago Extra: {p_u:,.2f}€\n"

        st.download_button("💾 GRABAR INFORME (.TXT)", informe_txt, file_name=f"informe_{st.session_state.nombre}.txt")
        if st.button("⬅️ VOLVER AL MENÚ", key="down"): st.session_state.seccion = 'menu'; st.rerun()

elif st.session_state.seccion == 'atrasos':
    st.markdown(f'<p class="titulo">💸 ATRASOS: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER"): st.session_state.seccion = 'menu'; st.rerun()
    with st.expander("⚙️ DATOS ATRASOS", expanded=True):
        p_ant_atr = st.number_input("Precio Hora ANTIGUO (€)", value=10.00, format="%.2f")
        h_sem_atr = st.number_input("Cómputo Semanal ACTUAL", value=40.0)
        cat_atr = st.selectbox("Categoría Original", list(TRAMOS_BASE.keys()))
        mes_h = st.selectbox("Calcular hasta:", MESES)

    if st.button("🚀 CALCULAR"):
        h_mens = (h_sem_atr * 44.2) / 12
        p_n = motor_2026(p_ant_atr, h_sem_atr, cat_atr)
        total = (p_n - p_ant_atr) * h_mens * (MESES.index(mes_h) + 1)
        st.markdown(f'<div class="card-anio"><span class="val-new">TOTAL ATRASOS: {total:,.2f} € bruto</span></div>', unsafe_allow_html=True)
