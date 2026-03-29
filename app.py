import streamlit as st
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="Gestor Convenio 26-29 Pro", layout="centered")

# ESTILO DE ALTO IMPACTO (RESTAURADO E ÍNTEGRO)
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], header, footer { display: none !important; visibility: hidden !important; }
    .stApp { background: #0a0f1e; padding-top: 0px !important; }
    .titulo { text-align: center; color: #ffffff; font-size: 26px; font-weight: 800; margin-bottom: 20px; text-transform: uppercase; }
    label { color: #ffffff !important; font-weight: 800 !important; font-size: 15px !important; }
    .card-anio { background: #1e293b; border: 1px solid #475569; border-radius: 14px; padding: 18px; margin-bottom: 20px; }
    .col-dato { background: #0f172a; padding: 12px; border-radius: 10px; border-left: 4px solid #3b82f6; margin-bottom: 10px; }
    .label-dato { color: #94a3b8; font-size: 11px; text-transform: uppercase; font-weight: 700; margin-bottom: 4px; }
    .val-old { color: #cbd5e1; font-size: 13px; display: block; margin-bottom: 2px; }
    .val-new { color: #ffffff; font-size: 19px; font-weight: 800; display: block; }
    .pago-mano { background: rgba(245, 158, 11, 0.15); border: 1px dashed #f59e0b; color: #fbbf24; padding: 10px; border-radius: 8px; margin-top: 15px; text-align: center; font-weight: 700; }
    .stButton>button { width: 100%; background-color: #2563eb !important; color: white !important; font-weight: bold !important; height: 50px; border-radius: 10px; margin-bottom: 10px; }
    div[data-testid="stMarkdownContainer"] p { color: #ffffff !important; }
    .badge-inc { background: #10b981; color: white; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; }
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
    st.markdown(f'<p class="titulo">📅 DESGLOSE DOM/FES: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ", key="up_fes"): st.session_state.seccion = 'menu'; st.rerun()
    with st.expander("⚙️ DATOS DE HORAS", expanded=True):
        cat_f = st.selectbox("Categoría Profesional", list(TRAMOS_BASE.keys()))
        p_ant_f = st.number_input("Precio Hora ANTIGUO (€)", value=10.00, format="%.2f")
        h_dom = st.number_input("Horas DOMINGOS", value=0.0)
        h_fes = st.number_input("Horas FESTIVOS", value=0.0)

    if st.button("🚀 CALCULAR DESGLOSE"):
        p_new_f = motor_2026(p_ant_f, 40.0, cat_f)
        # Lógica Domingos: Base + Plus (50 o 60) por cada 8h
        plus_8h = 50.0 if "Cajer" in cat_f else 60.0
        p_h_dom_ant = p_ant_f + (plus_8h / 8)
        p_h_dom_new = p_new_f * 2
        dif_dom = (p_h_dom_new - p_h_dom_ant) * h_dom
        # Festivos: 1.5 sobre base
        p_h_fes_ant = p_ant_f * 1.5
        p_h_fes_new = p_new_f * 1.5
        dif_fes = (p_h_fes_new - p_h_fes_ant) * h_fes
        
        st.markdown(f"""
            <div class="card-anio">
                <p class="label-dato">Desglose Domingos</p>
                <div class="col-dato">
                    <span class="val-old">Precio antiguo (Base + Plus): {p_h_dom_ant:.2f} €/h</span>
                    <span class="val-new">Precio nuevo (Base x 2): {p_h_dom_new:.2f} €/h</span>
                    <span style="color:#10b981; font-weight:bold;">Atraso Dom: {dif_dom:,.2f} €</span>
                </div>
                <p class="label-dato">Desglose Festivos</p>
                <div class="col-dato">
                    <span class="val-old">Precio antiguo (x1.5): {p_h_fes_ant:.2f} €/h</span>
                    <span class="val-new">Precio nuevo (x1.5): {p_h_fes_new:.2f} €/h</span>
                    <span style="color:#10b981; font-weight:bold;">Atraso Fes: {dif_fes:,.2f} €</span>
                </div>
                <div class="pago-mano" style="font-size:20px;">TOTAL: {(dif_dom + dif_fes):,.2f} € bruto</div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ VOLVER AL MENÚ", key="down_fes"): st.session_state.seccion = 'menu'; st.rerun()
        with col2:
            txt_fes = f"INFORME FESTIVOS - {st.session_state.nombre}\n\nAtraso Domingos: {dif_dom:.2f} EUR\nAtraso Festivos: {dif_fes:.2f} EUR\nTOTAL: {(dif_dom+dif_fes):.2f} EUR"
            st.download_button("💾 IMPRIMIR (.TXT)", data=txt_fes, file_name="festivos.txt")

elif st.session_state.seccion == 'subida':
    st.markdown(f'<p class="titulo">📈 PROYECCIÓN: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ", key="up_sub"): st.session_state.seccion = 'menu'; st.rerun()
    with st.expander("⚙️ CONFIGURACIÓN", expanded=True):
        p_act = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
        h_ant_i = st.number_input("Cómputo Semanal ACTUAL", value=40.0)
        h_new_i = st.number_input("Cómputo Semanal PRÓXIMO", value=40.0)
        pagas = st.selectbox("Número de Pagas", [12, 14])
        cat = st.selectbox("Categoría", list(TRAMOS_BASE.keys()))
        vista = st.selectbox("Vista", ["2026", "2027", "2028", "2029", "COMPLETO"])

    if st.button("🚀 CALCULAR PROYECCIÓN"):
        h_an_ant, h_an_new = h_ant_i * 44.2, h_new_i * 44.2
        f_j, p_acum = h_new_i / 40, p_act
        limite = 2029 if vista == "COMPLETO" else int(vista)
        total_con_subida, total_sin_subida = 0, 0
        txt_informe = f"INFORME DE PROYECCIÓN SALARIAL - {st.session_state.nombre}\n" + "="*40 + "\n"
        
        for anio in range(2026, limite + 1):
            h_ref = h_an_ant if anio == 2026 else h_an_new
            p_prev = p_acum
            fijo, mano_pct = (1.04, 0.02) if anio == 2026 else (1.03, 0.015)
            tramos_anio = TRAMOS_BASE[cat].copy()
            factor_tramos = (1.03 ** (anio - 2026))
            ult_tramo_aj = tramos_anio[-1] * factor_tramos * f_j
            sal_fijo = (p_prev * h_an_new) * fijo
            n_anual, p_u = 0, 0.0
            if sal_fijo >= (ult_tramo_aj - 0.01):
                n_anual, p_u = sal_fijo, (p_prev * h_ref) * mano_pct
            else:
                n_anual = sal_fijo
                for t in tramos_anio:
                    t_val = t * factor_tramos * f_j
                    if sal_fijo < t_val: n_anual = t_val; break
            p_acum = n_anual / h_an_new
            m_new = (n_anual / pagas)
            inc = ((p_acum / p_prev) - 1) * 100
            total_con_subida += (n_anual + p_u)
            total_sin_subida += (p_act * h_an_new)
            
            txt_informe += f"\nAÑO {anio}:\n- Precio Hora: {p_acum:.2f} €\n- Salario Mensual: {m_new:,.2f} €\n- Incremento: {inc:.2f}%"
            if p_u > 0: txt_informe += f"\n- Pago Mano Alzada: {p_u:,.2f} €"
            txt_informe += "\n" + "-"*20

            st.markdown(f"""
                <div class="card-anio">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span style="color:white; font-size:19px; font-weight:800;">AÑO {anio}</span>
                        <span class="badge-inc">+{inc:.2f}%</span>
                    </div>
                    <div class="grid-datos">
                        <div class="col-dato"><p class="label-dato">Precio Hora</p><span class="val-old">Antes: {p_prev:.2f} €</span><span class="val-new">{p_acum:.2f} €</span></div>
                        <div class="col-dato"><p class="label-dato">Mensual ({pagas} pagas)</p><span class="val-new">{m_new:,.2f} €</span></div>
                    </div>
                    {f'<div class="pago-mano">💰 PAGO MANO ALZADA: {p_u:,.2f} €</div>' if p_u > 0 else ""}
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
            <div class="card-anio" style="border: 2px solid #3b82f6; background: #0f172a;">
                <p class="titulo" style="font-size:18px; margin-bottom:10px;">📊 RESUMEN FINAL</p>
                <div class="col-dato">
                    <p class="label-dato">Total acumulado CON subidas</p>
                    <span class="val-new" style="color:#10b981;">{total_con_subida:,.2f} €</span>
                </div>
                <div class="col-dato">
                    <p class="label-dato">Total acumulado SIN subidas</p>
                    <span class="val-new" style="color:#94a3b8;">{total_sin_subida:,.2f} €</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ VOLVER AL MENÚ", key="down_sub"): st.session_state.seccion = 'menu'; st.rerun()
        with col2:
            txt_informe += f"\n\nRESUMEN FINAL:\nTOTAL CON SUBIDAS: {total_con_subida:,.2f} €\nTOTAL SIN SUBIDAS: {total_sin_subida:,.2f} €"
            st.download_button("💾 IMPRIMIR (.TXT)", data=txt_informe, file_name="subida_salarial.txt")

elif st.session_state.seccion == 'atrasos':
    st.markdown(f'<p class="titulo">💸 ATRASOS 2026: {st.session_state.nombre}</p>', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ", key="up_atr"): st.session_state.seccion = 'menu'; st.rerun()
    with st.expander("⚙️ CONFIGURACIÓN", expanded=True):
        p_ant_atr = st.number_input("Precio Hora 2025 (€)", value=10.00, format="%.2f")
        h_sem_atr = st.number_input("Horas Semanales", value=40.0)
        cat_atr = st.selectbox("Categoría para tramos", list(TRAMOS_BASE.keys()))
        mes_hasta = st.select_slider("Calcular hasta el mes de:", options=MESES, value="Mayo")

    if st.button("🚀 CALCULAR ATRASOS"):
        p_nuevo_atr = motor_2026(p_ant_atr, h_sem_atr, cat_atr)
        dif_hora = p_nuevo_atr - p_ant_atr
        h_mensuales = h_sem_atr * 4.33
        num_meses = MESES.index(mes_hasta) + 1
        total_atrasos = dif_hora * h_mensuales * num_meses
        
        st.markdown(f"""
            <div class="card-anio">
                <p class="label-dato">Resultado del Cálculo</p>
                <div class="col-dato">
                    <span class="val-old">Incremento por hora: {dif_hora:.4f} €</span>
                    <span class="val-new">Mensual estimado: {(dif_hora * h_mensuales):,.2f} €</span>
                </div>
                <div class="pago-mano" style="font-size:20px;">ATRASOS TOTALES ({mes_hasta}): {total_atrasos:,.2f} €</div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ VOLVER AL MENÚ", key="down_atr"): st.session_state.seccion = 'menu'; st.rerun()
        with col2:
            st.download_button("💾 IMPRIMIR (.TXT)", f"INFORME ATRASOS - {st.session_state.nombre}\n\nMes hasta: {mes_hasta}\nTotal Atrasos: {total_atrasos:.2f} €", "atrasos.txt")

elif st.session_state.seccion == 'salir':
    st.markdown('<p class="titulo">👋 ¡HASTA PRONTO!</p>', unsafe_allow_html=True)
    if st.button("VOLVER A ENTRAR"): st.session_state.seccion = 'menu'; st.rerun()
