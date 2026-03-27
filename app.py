import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Gestión Convenio 2026-2029", layout="centered")

# Estilo Global (Alto contraste para móvil)
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; }
    .titulo-principal { text-align: center; color: #ffffff; font-size: 26px; font-weight: 800; margin-bottom: 30px; }
    label { color: #ffffff !important; font-weight: 700 !important; }
    .stButton>button { width: 100%; border-radius: 10px; height: 50px; font-weight: bold; }
    .card { background: #1e293b; border: 1px solid #475569; border-radius: 14px; padding: 18px; margin-bottom: 20px; }
    .val-new { color: #10b981; font-size: 22px; font-weight: 800; }
    .pago-mano { background: rgba(245, 158, 11, 0.2); border: 2px dashed #f59e0b; color: #fbbf24; padding: 12px; border-radius: 10px; text-align: center; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# Tramos Base 2026
TRAMOS = {
    "Cajer@/Reponedor": [18800, 19800, 21000],
    "Asistent@ / Oficial": [21000, 22000, 23000],
    "Adjunt@": [25000, 27000, 29000],
    "Gt": [29500, 31000, 33600, 35000, 38200]
}

# --- ESTADO DE NAVEGACIÓN ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'menu'

def ir_a(nombre):
    st.session_state.pagina = nombre

# --- VISTA: MENÚ PRINCIPAL ---
if st.session_state.pagina == 'menu':
    st.markdown('<p class="titulo-principal">📊 GESTIÓN CONVENIO 2026-2029</p>', unsafe_allow_html=True)
    st.button("📈 SUBIDA SALARIAL", on_click=ir_a, args=('subida',))
    st.button("💸 CÁLCULO DE ATRASOS", on_click=ir_a, args=('atrasos',))
    st.button("🚪 SALIR", on_click=ir_a, args=('salir',))

# --- VISTA: SALIR ---
elif st.session_state.pagina == 'salir':
    st.success("Sesión cerrada. Puedes cerrar la pestaña del navegador.")
    if st.button("↩️ Volver a entrar"):
        ir_a('menu')
        st.rerun()

# --- VISTA: ATRASOS ---
elif st.session_state.pagina == 'atrasos':
    st.markdown('<p class="titulo-principal">💸 CÁLCULO DE ATRASOS</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): ir_a('menu'); st.rerun()
    
    with st.form("form_atrasos"):
        mes_hasta = st.selectbox("Atrasos hasta el mes de:", ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
        cat_atr = st.selectbox("Categoría", list(TRAMOS.keys()))
        jornada_mensual = st.number_input("Horas Mensuales (Ej: 170)", value=170.0)
        p_ant_atr = st.number_input("Precio Hora ANTIGUO (€)", value=10.00, format="%.2f")
        p_new_atr = st.number_input("Precio Hora NUEVO (€)", value=10.40, format="%.2f")
        
        btn_calc_atr = st.form_submit_button("CALCULAR ATRASOS")
        
        if btn_calc_atr:
            meses_lista = ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            num_meses = meses_lista.index(mes_hasta) + 1
            dif_hora = p_new_atr - p_ant_atr
            total_atrasos = dif_hora * jornada_mensual * num_meses
            
            st.markdown(f"""
                <div class="card" style="border-left: 8px solid #f59e0b;">
                    <p style="color:white; margin-bottom:5px;">Diferencia por hora: <b>{dif_hora:.2f} €</b></p>
                    <p style="color:white; margin-bottom:5px;">Meses acumulados (desde Marzo): <b>{num_meses}</b></p>
                    <hr>
                    <p style="color:#f59e0b; font-size:14px;">TOTAL ATRASOS BRUTOS</p>
                    <p class="val-new">{total_atrasos:,.2f} €</p>
                </div>
            """, unsafe_allow_html=True)

# --- VISTA: SUBIDA SALARIAL (LOGICA ANTERIOR) ---
elif st.session_state.pagina == 'subida':
    st.markdown('<p class="titulo-principal">📈 PROYECCIÓN SALARIAL</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): ir_a('menu'); st.rerun()
    
    with st.expander("⚙️ CONFIGURAR DATOS", expanded=True):
        p_act = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
        h_ant = st.number_input("Horas Actuales", value=40.0)
        h_new = st.number_input("Horas Nuevo Convenio", value=40.0)
        pagas = st.selectbox("Pagas", [12, 14, 15])
        cat = st.selectbox("Categoría", list(TRAMOS.keys()))
        vista = st.selectbox("Hasta el año:", ["2026", "2027", "2028", "2029", "COMPLETO"])

    if st.button("🚀 CALCULAR"):
        h_an_ant, h_an_new = h_ant * 44.2, h_new * 44.2
        f_jornada = h_new / 40
        limite = 2029 if vista == "COMPLETO" else int(vista)
        p_acum = p_act

        for anio in range(2026, limite + 1):
            h_ref = h_an_ant if anio == 2026 else h_an_new
            p_prev = p_acum
            a_prev = p_prev * h_ref
            
            fijo = 1.04 if anio == 2026 else 1.03
            mano_pct = 0.02 if anio == 2026 else 0.015
            
            tramos_anio = TRAMOS[cat].copy()
            tramos_anio[-1] *= (1.03 ** (anio - 2026))
            ultimo_tramo_limite = tramos_anio[-1] * f_jornada
            
            sal_fijo = (p_prev * h_an_new) * fijo
            p_u = 0.0

            if sal_fijo >= (ultimo_tramo_limite - 0.01):
                n_anual = sal_fijo
                p_u = a_prev * mano_pct
            else:
                n_anual = sal_fijo
                for t in tramos_anio:
                    t_aj = t * f_jornada
                    if sal_fijo < t_aj:
                        n_anual = t_aj; break
            
            p_acum = n_anual / h_an_new
            st.markdown(f"""
                <div class="card">
                    <div style="display:flex; justify-content:space-between;"><b>{anio}</b> <span style="color:#10b981;">+{((p_acum/p_prev)-1)*100:.2f}%</span></div>
                    <div style="color:#94a3b8; font-size:12px; margin-top:10px;">PRECIO HORA</div>
                    <div class="val-new">{p_acum:.2f} €</div>
                    {f'<div class="pago-mano">💰 PAGO MANO ALZADA: {p_u:,.2f} €</div>' if p_u > 0 else ""}
                </div>
            """, unsafe_allow_html=True)
