import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Gestión Convenio Pro", layout="centered")

# Estilo de Alto Contraste (Igual al exitoso anterior)
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; }
    .titulo { text-align: center; color: #ffffff; font-size: 26px; font-weight: 800; margin-bottom: 20px; text-transform: uppercase; }
    label { color: #ffffff !important; font-weight: 800 !important; font-size: 15px !important; }
    
    .card-anio {
        background: #1e293b; border: 1px solid #475569; border-radius: 14px;
        padding: 18px; margin-bottom: 20px;
    }
    .header-anio { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #475569; padding-bottom: 10px; }
    .badge-inc { background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: 700; }
    
    .grid-datos { display: flex; flex-direction: column; gap: 10px; }
    @media (min-width: 600px) { .grid-datos { flex-direction: row; justify-content: space-between; } .col-dato { flex: 1; } }
    
    .col-dato { background: #0f172a; padding: 10px; border-radius: 8px; border-left: 4px solid #3b82f6; }
    .label-dato { color: #94a3b8; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .val-old { color: #cbd5e1; font-size: 13px; display: block; }
    .val-new { color: #ffffff; font-size: 20px; font-weight: 800; display: block; }
    
    .pago-mano { background: rgba(245, 158, 11, 0.2); border: 2px dashed #f59e0b; color: #fbbf24; padding: 12px; border-radius: 10px; margin-top: 15px; text-align: center; font-weight: 800; }
    
    /* Botones del Menú Principal */
    .btn-menu button { height: 60px !important; font-size: 18px !important; margin-bottom: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# Tramos Base 2026
TRAMOS = {
    "Cajer@/Reponedor": [18800, 19800, 21000],
    "Asistent@ / Oficial": [21000, 22000, 23000],
    "Adjunt@": [25000, 27000, 29000],
    "Gt": [29500, 31000, 33600, 35000, 38200]
}

if 'seccion' not in st.session_state:
    st.session_state.seccion = 'menu'

# --- NAVEGACIÓN ---
if st.session_state.seccion == 'menu':
    st.markdown('<p class="titulo">📱 MENÚ PRINCIPAL</p>', unsafe_allow_html=True)
    if st.button("📈 SUBIDA SALARIAL", key="btn_subida"): st.session_state.seccion = 'subida'; st.rerun()
    if st.button("💸 CÁLCULO DE ATRASOS", key="btn_atrasos"): st.session_state.seccion = 'atrasos'; st.rerun()
    if st.button("🚪 SALIR", key="btn_salir"): st.session_state.seccion = 'salir'; st.rerun()

elif st.session_state.seccion == 'salir':
    st.markdown('<p class="titulo">SESIÓN FINALIZADA</p>', unsafe_allow_html=True)
    if st.button("↩️ REINICIAR"): st.session_state.seccion = 'menu'; st.rerun()

# --- SECCIÓN: ATRASOS ---
elif st.session_state.seccion == 'atrasos':
    st.markdown('<p class="titulo">💸 CÁLCULO DE ATRASOS</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER"): st.session_state.seccion = 'menu'; st.rerun()
    
    with st.expander("⚙️ DATOS PARA ATRASOS", expanded=True):
        mes_fin = st.selectbox("Atrasos hasta el mes de:", ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
        h_semanales = st.number_input("Horas Semanales", value=40.0)
        p_antiguo = st.number_input("Precio Hora Antiguo (€)", value=10.00, format="%.2f")
        p_nuevo = st.number_input("Precio Hora Nuevo (€)", value=10.40, format="%.2f")

    if st.button("🚀 CALCULAR ATRASOS"):
        meses_nombres = ["Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        num_meses = meses_nombres.index(mes_fin) + 1
        # Cálculo: (Horas sem * 44.2 semanas / 12 meses) = Horas mes promedio
        h_mensuales_promedio = (h_semanales * 44.2) / 12
        dif_precio = p_nuevo - p_antiguo
        total_atrasos = dif_precio * h_mensuales_promedio * num_meses
        
        st.markdown(f"""
            <div class="card-anio" style="border-left: 8px solid #f59e0b;">
                <p class="label-dato">Resultado del Cálculo</p>
                <span class="val-new">{total_atrasos:,.2f} € Brutos</span>
                <p style="color:#cbd5e1; font-size:14px; margin-top:10px;">
                    Diferencia: {dif_precio:.2f} €/hora<br>
                    Horas mes: {h_mensuales_promedio:.2f}<br>
                    Meses acumulados: {num_meses}
                </p>
            </div>
        """, unsafe_allow_html=True)

# --- SECCIÓN: SUBIDA SALARIAL ---
elif st.session_state.seccion == 'subida':
    st.markdown('<p class="titulo">📈 SUBIDA SALARIAL</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER"): st.session_state.seccion = 'menu'; st.rerun()
    
    with st.expander("⚙️ CONFIGURAR DATOS", expanded=True):
        p_act = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
        h_ant = st.number_input("Horas Semanales Actuales", value=40.0)
        h_new = st.number_input("Horas Nuevo Convenio", value=40.0)
        pagas = st.selectbox("Pagas", [12, 14])
        cat = st.selectbox("Categoría", list(TRAMOS.keys()))
        vista = st.selectbox("Proyectar hasta:", ["2026", "2027", "2028", "2029", "COMPLETO"])

    if st.button("🚀 CALCULAR PROYECCIÓN"):
        h_an_ant, h_an_new = h_ant * 44.2, h_new * 44.2
        f_jornada = h_new / 40
        limite = 2029 if vista == "COMPLETO" else int(vista)
        p_acum = p_act

        for anio in range(2026, limite + 1):
            h_ref = h_an_ant if anio == 2026 else h_an_new
            p_prev = p_acum
            a_prev, m_prev = p_prev * h_ref, (p_prev * h_ref) / pagas
            
            fijo, mano_pct = (1.04, 0.02) if anio == 2026 else (1.03, 0.015)
            
            tramos_anio = TRAMOS[cat].copy()
            tramos_anio[-1] *= (1.03 ** (anio - 2026))
            limite_ultimo_tramo = tramos_anio[-1] * f_jornada
            
            sal_fijo = (p_prev * h_an_new) * fijo
            n_anual, p_u = 0, 0.0

            if sal_fijo >= (limite_ultimo_tramo - 0.01):
                n_anual, p_u = sal_fijo, a_prev * mano_pct
            else:
                n_anual = sal_fijo
                for t in tramos_anio:
                    t_aj = t * f_jornada
                    if sal_fijo < t_aj: n_anual = t_aj; break

            p_acum = n_anual / h_an_new
            m_new = n_anual / pagas
            inc_anual = ((p_acum / p_prev) - 1) * 100

            st.markdown(f"""
                <div class="card-anio">
                    <div class="header-anio">
                        <span style="color:white; font-size:18px; font-weight:800;">AÑO {anio}</span>
                        <span class="badge-inc">+{inc_anual:.2f}% Nómina</span>
                    </div>
                    <div class="grid-datos">
                        <div class="col-dato"><p class="label-dato">Precio Hora</p><span class="val-old">Antes: {p_prev:.2f} €</span><span class="val-new">{p_acum:.2f} €</span></div>
                        <div class="col-dato"><p class="label-dato">Mensual</p><span class="val-old">Antes: {m_prev:,.2f} €</span><span class="val-new">{m_new:,.2f} €</span></div>
                        <div class="col-dato"><p class="label-dato">Anual</p><span class="val-old">Antes: {a_prev:,.2f} €</span><span class="val-new">{n_anual:,.2f} €</span></div>
                    </div>
                    {f'<div class="pago-mano">💰 PAGO A MANO ALZADA ({round(mano_pct*100,1)}%): {p_u:,.2f} €</div>' if p_u > 0 else ""}
                </div>
            """, unsafe_allow_html=True)
