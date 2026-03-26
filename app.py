import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Simulador Salarial 26-29", layout="centered")

# Estilo Optimizado: Contraste alto para etiquetas
st.markdown("""
    <style>
    .stApp { background: #0f172a; }
    .titulo { text-align: center; color: #f8fafc; font-size: 24px; font-weight: 800; margin-bottom: 20px; }
    
    /* Forzar color blanco en los textos de los inputs */
    label { color: #ffffff !important; font-weight: 600 !important; font-size: 14px !important; }
    
    .card-anio {
        background: #1e293b; border: 1px solid #334155; border-radius: 12px;
        padding: 15px; margin-bottom: 15px;
    }
    .header-anio { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #334155; padding-bottom: 8px; }
    .badge-inc { background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; }
    
    .grid-datos { display: flex; flex-direction: column; gap: 10px; }
    @media (min-width: 600px) {
        .grid-datos { flex-direction: row; justify-content: space-between; }
        .col-dato { flex: 1; }
    }
    
    .col-dato { background: #0f172a; padding: 10px; border-radius: 8px; border-left: 4px solid #3b82f6; }
    .label-dato { color: #94a3b8; font-size: 10px; text-transform: uppercase; font-weight: 600; }
    .val-old { color: #94a3b8; font-size: 13px; display: block; }
    .val-new { color: #ffffff; font-size: 18px; font-weight: 700; display: block; }
    
    .pago-extra { background: rgba(245, 158, 11, 0.1); border: 1px solid #f59e0b; color: #fbbf24; padding: 8px; border-radius: 6px; margin-top: 10px; text-align: center; font-size: 13px; font-weight: bold; }
    
    /* Expander con fondo más claro para visibilidad */
    .streamlit-expanderHeader { background-color: #1e293b !important; color: white !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">📊 SIMULADOR CONVENIO 2026-2029</p>', unsafe_allow_html=True)

# --- CONFIGURACIÓN DE DATOS ---
with st.expander("⚙️ CONFIGURAR DATOS (Toca aquí para editar)", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        p_actual_input = st.number_input("Precio Hora ACTUAL (€)", value=10.00, format="%.2f")
        h_sem_ant = st.number_input("Horas Semanales ACTUALES", value=40.0)
    with col_b:
        h_sem_new = st.number_input("Horas Semanales NUEVO CONVENIO", value=40.0)
        n_pagas = st.selectbox("Número de Pagas", [12, 14, 15])
    
    cat = st.selectbox("Categoría Profesional", ["Cajer@/Reponedor", "Asistent@ / Oficial", "Adjunt@", "Gt"])
    vista = st.selectbox("Ver evolución hasta el año:", ["2026", "2027", "2028", "2029", "COMPLETO"])

if st.button("🚀 GENERAR INFORME ACTUALIZADO"):
    tramos_base = {
        "Cajer@/Reponedor": [18800, 19800, 21000],
        "Asistent@ / Oficial": [21000, 22000, 23000],
        "Adjunt@": [25000, 27000, 29000],
        "Gt": [29500, 31000, 33600, 35000, 38200]
    }
    
    # Cálculo inicial (Estado Actual)
    h_anuales_ant = h_sem_ant * 44.2
    h_anuales_new = h_sem_new * 44.2
    f_jornada_new = h_sem_new / 40
    
    limite = 2029 if vista == "COMPLETO" else int(vista)
    anios_rango = list(range(2026, limite + 1))
    
    p_acumulado = p_actual_input

    for anio in anios_rango:
        p_ant = p_acumulado
        # El mensual anterior se calcula con las horas que tenías antes de este ciclo
        m_ant = (p_ant * (h_sem_ant * 44.2 if anio == 2026 else h_sem_new * 44.2)) / n_pagas
        a_ant = p_ant * (h_sem_ant * 44.2 if anio == 2026 else h_sem_new * 44.2)
        
        fijo = 1.04 if anio == 2026 else 1.03
        unico = 0.02 if anio == 2026 else 0.015
        
        # Proyectamos con la nueva jornada
        salario_base_calculo = p_ant * h_anuales_new
        salario_con_fijo = salario_base_calculo * fijo
        
        # Ajuste de tramos: Solo el último sube el 3% anual acumulado
        tramos_anio = tramos_base[cat].copy()
        inc_ultimo_tramo = 1.03 ** (anio - 2026)
        tramos_anio[-1] = tramos_anio[-1] * inc_ultimo_tramo
        
        n_anual, p_u, encontrado = 0, 0.0, False
        for t in tramos_anio:
            t_ajustado = t * f_jornada_new
            if salario_con_fijo < t_ajustado:
                n_anual = t_ajustado
                encontrado = True
                break
        
        if not encontrado:
            n_anual = salario_con_fijo
            p_u = salario_base_calculo * unico
            
        p_acumulado = n_anual / h_anuales_new
        m_new = n_anual / n_pagas
        inc_anual = ((p_acumulado / p_ant) - 1) * 100

        # --- RENDERIZADO ---
        st.markdown(f"""
            <div class="card-anio">
                <div class="header-anio">
                    <span style="color:white; font-size:18px; font-weight:800;">EJERCICIO {anio}</span>
                    <span class="badge-inc">+{inc_anual:.2f}% Incremento</span>
                </div>
                <div class="grid-datos">
                    <div class="col-dato">
                        <p class="label-dato">Precio Hora</p>
                        <span class="val-old">Antes: {p_ant:.2f} €</span>
                        <span class="val-new">{p_acumulado:.2f} €</span>
                    </div>
                    <div class="col-dato">
                        <p class="label-dato">Mensual ({n_pagas} pagas)</p>
                        <span class="val-old">Antes: {m_ant:,.2f} €</span>
                        <span class="val-new">{m_new:,.2f} €</span>
                    </div>
                    <div class="col-dato">
                        <p class="label-dato">Bruto Anual</p>
                        <span class="val-old">Antes: {a_ant:,.2f} €</span>
                        <span class="val-new">{n_anual:,.2f} €</span>
                    </div>
                </div>
                {f'<div class="pago-extra">💰 Pago Único Consolidado: {p_u:,.2f} €</div>' if p_u > 0 else ""}
            </div>
        """, unsafe_allow_html=True)
