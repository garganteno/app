import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Gestor Convenio 26-29", layout="centered")

# Estilo de Alto Contraste (Blanco sobre Negro/Azul)
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; }
    .titulo { text-align: center; color: #ffffff; font-size: 26px; font-weight: 800; margin-bottom: 20px; text-transform: uppercase; }
    label { color: #ffffff !important; font-weight: 800 !important; font-size: 14px !important; }
    .card-anio { background: #1e293b; border: 1px solid #475569; border-radius: 14px; padding: 18px; margin-bottom: 20px; }
    .header-anio { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #475569; padding-bottom: 10px; }
    .badge-inc { background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: 700; }
    .grid-datos { display: flex; flex-direction: column; gap: 10px; }
    @media (min-width: 600px) { .grid-datos { flex-direction: row; justify-content: space-between; } .col-dato { flex: 1; } }
    .col-dato { background: #0f172a; padding: 10px; border-radius: 8px; border-left: 4px solid #3b82f6; }
    .label-dato { color: #94a3b8; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .val-old { color: #cbd5e1; font-size: 13px; display: block; }
    .val-new { color: #ffffff; font-size: 19px; font-weight: 800; display: block; }
    .pago-mano { background: rgba(245, 158, 11, 0.2); border: 2px dashed #f59e0b; color: #fbbf24; padding: 12px; border-radius: 10px; margin-top: 15px; text-align: center; font-weight: 800; }
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

if 'seccion' not in st.session_state:
    st.session_state.seccion = 'menu'

# --- FUNCIÓN MOTOR DE CÁLCULO 2026 ---
def motor_2026(p_ant, h_sem, cat):
    h_an = h_sem * 44.2
    f_j = h_sem / 40
    sal_proy = (p_ant * h_an) * 1.04
    tramos = TRAMOS_BASE[cat].copy()
    ult_tramo = tramos[-1] * f_j
    if sal_proy >= (ult_tramo - 0.01):
        return sal_proy / h_an
    for t in tramos:
        t_aj = t * f_j
        if sal_proy < t_aj: return t_aj / h_an
    return sal_proy / h_an

# --- NAVEGACIÓN ---
if st.session_state.seccion == 'menu':
    st.markdown('<p class="titulo">📱 GESTIÓN CONVENIO 26-29</p>', unsafe_allow_html=True)
    if st.button("📈 SUBIDA SALARIAL"): st.session_state.seccion = 'subida'; st.rerun()
    if st.button("💸 CÁLCULO DE ATRASOS"): st.session_state.seccion = 'atrasos'; st.rerun()
    if st.button("🚪 SALIR"): st.session_state.seccion = 'salir'; st.rerun()

elif st.session_state.seccion == 'salir':
    st.markdown('<p class="titulo">SESIÓN FINALIZADA</p>', unsafe_allow_html=True)
    if st.button("↩️ REINICIAR"): st.session_state.seccion = 'menu'; st.rerun()

# --- VISTA: ATRASOS ---
elif st.session_state.seccion == 'atrasos':
    st.markdown('<p class="titulo">💸 ATRASOS 2026</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): st.session_state.seccion = 'menu'; st.rerun()
    
    with st.expander("⚙️ DATOS DE ATRASOS", expanded=True):
        p_ant_atr = st.number_input("Precio Hora ANTIGUO (€)", value=10.00, format="%.2f")
        h_sem_atr = st.number_input("Horas Semanales", value=40.0)
        cat_atr = st.selectbox("Categoría Original", list(TRAMOS_BASE.keys()))
        cambio = st.radio("¿Hubo cambio de categoría?", ["No", "Si"], horizontal=True)
        if cambio == "Si":
            mes_c = st.selectbox("Mes del cambio:", MESES)
            cat_n = st.selectbox("Nueva Categoría:", list(TRAMOS_BASE.keys()))
        mes_h = st.selectbox("Calcular hasta el mes de:", MESES)

    if st.button("🚀 CALCULAR"):
        h_mens = (h_sem_atr * 44.2) / 12
        idx_hasta = MESES.index(mes_h) + 1
        if cambio == "No":
            p_n = motor_2026(p_ant_atr, h_sem_atr, cat_atr)
            total = (p_n - p_ant_atr) * h_mens * idx_hasta
        else:
            idx_c = MESES.index(mes_c)
            p_n1 = motor_2026(p_ant_atr, h_sem_atr, cat_atr)
            m1 = min(idx_hasta, idx_c)
            a1 = (p_n1 - p_ant_atr) * h_mens * m1
            a2 = 0.0
            if idx_hasta > idx_c:
                p_n2 = motor_2026(p_ant_atr, h_sem_atr, cat_n)
                m2 = idx_hasta - idx_c
                a2 = (p_n2 - p_ant_atr) * h_mens * m2
            total = a1 + a2
        st.markdown(f'<div class="card-anio" style="border-left:8px solid #f59e0b;"><p class="label-dato">TOTAL ATRASOS BRUTOS</p><span class="val-new">{total:,.2f} €</span></div>', unsafe_allow_html=True)

# --- VISTA: SUBIDA SALARIAL ---
elif st.session_state.seccion == 'subida':
    st.markdown('<p class="titulo">📈 PROYECCIÓN 26-29</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): st.session_state.seccion = 'menu'; st.rerun()
    
    with st.expander("⚙️ CONFIGURACIÓN", expanded=True):
        p_act = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
        h_ant = st.number_input("Horas Semanales Actuales", value=40.0)
        h_new = st.number_input("Horas Nuevo Convenio", value=40.0)
        pagas = st.selectbox("Número de Pagas", [12, 14])
        cat = st.selectbox("Categoría Profesional", list(TRAMOS_BASE.keys()))
        vista = st.selectbox("Proyectar hasta:", ["2026", "2027", "2028", "2029", "COMPLETO"])

    if st.button("🚀 CALCULAR PROYECCIÓN"):
        h_an_ant, h_an_new = h_ant * 44.2, h_new * 44.2
        f_j = h_new / 40
        limite = 2029 if vista == "COMPLETO" else int(vista)
        p_acum = p_act

        for anio in range(2026, limite + 1):
            h_ref = h_an_ant if anio == 2026 else h_an_new
            p_prev = p_acum
            a_prev, m_prev = p_prev * h_ref, (p_prev * h_ref) / pagas
            fijo, mano_pct = (1.04, 0.02) if anio == 2026 else (1.03, 0.015)
            
            tramos_anio = TRAMOS_BASE[cat].copy()
            tramos_anio[-1] *= (1.03 ** (anio - 2026))
            ult_t_aj = tramos_anio[-1] * f_j
            
            sal_fijo = (p_prev * h_an_new) * fijo
            n_anual, p_u = 0, 0.0

            if sal_fijo >= (ult_t_aj - 0.01):
                n_anual, p_u = sal_fijo, a_prev * mano_pct
            else:
                n_anual = sal_fijo
                for t in tramos_anio:
                    t_aj = t * f_j
                    if sal_fijo < t_aj: n_anual = t_aj; break
            
            p_acum = n_anual / h_an_new
            m_new = n_anual / pagas
            inc = ((p_acum / p_prev) - 1) * 100

            st.markdown(f"""
                <div class="card-anio">
                    <div class="header-anio"><span style="color:white; font-size:18px; font-weight:800;">AÑO {anio}</span><span class="badge-inc">+{inc:.2f}%</span></div>
                    <div class="grid-datos">
                        <div class="col-dato"><p class="label-dato">Precio Hora</p><span class="val-old">Antes: {p_prev:.2f} €</span><span class="val-new">{p_acum:.2f} €</span></div>
                        <div class="col-dato"><p class="label-dato">Mensual ({pagas} pagas)</p><span class="val-old">Antes: {m_prev:,.2f} €</span><span class="val-new">{m_new:,.2f} €</span></div>
                        <div class="col-dato"><p class="label-dato">Anual Bruto</p><span class="val-old">Antes: {a_prev:,.2f} €</span><span class="val-new">{n_anual:,.2f} €</span></div>
                    </div>
                    {f'<div class="pago-mano">💰 PAGO MANO ALZADA: {p_u:,.2f} €</div>' if p_u > 0 else ""}
                </div>
            """, unsafe_allow_html=True)
