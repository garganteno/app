import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Simulador Salarial 26-29", layout="centered")

# Estilo Profesional
st.markdown("""
    <style>
    .stApp { background: #0f172a; }
    .titulo { text-align: center; color: #f8fafc; font-size: 30px; font-weight: 800; margin-bottom: 20px; }
    .card-resumen {
        background: #1e293b; border: 1px solid #334155; border-radius: 16px;
        padding: 20px; margin-bottom: 15px;
    }
    .grid-comparativa { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
    .data-box { background: #0f172a; padding: 12px; border-radius: 10px; border: 1px solid #334155; }
    .label-box { color: #94a3b8; font-size: 11px; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; }
    .val-old { color: #ef4444; font-size: 13px; text-decoration: line-through; display: block; opacity: 0.7; }
    .val-new { color: #10b981; font-size: 20px; font-weight: 700; display: block; }
    .badge-inc { background: #3b82f6; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 700; }
    .pago-unico { background: rgba(245, 158, 11, 0.1); border: 1px dashed #f59e0b; color: #fbbf24; 
                  padding: 8px; border-radius: 8px; margin-top: 10px; text-align: center; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">📊 SIMULADOR CONVENIO 2026-2029</p>', unsafe_allow_html=True)

# --- PANEL LATERAL ---
with st.sidebar:
    st.header("Datos Actuales")
    p_actual = st.number_input("Precio Hora (€)", value=10.0, format="%.2f")
    h_semanales = st.number_input("Horas Semanales", value=40.0)
    categoria = st.selectbox("Categoría", ["Cajer@/Reponedor", "Asistent@ / Oficial", "Adjunt@", "Gt"])
    pagas_anuales = st.selectbox("Pagas", [12, 14])
    modo = st.selectbox("Periodo", ["COMPLETO (4 años)", "2026", "2027", "2028", "2029"])

if st.button("CALCULAR INCREMENTOS PROFESIONALES"):
    tramos_base = {
        "Cajer@/Reponedor": [18800, 19800, 21000],
        "Asistent@ / Oficial": [21000, 22000, 23000],
        "Adjunt@": [25000, 27000, 29000],
        "Gt": [29500, 31000, 33600, 35000, 38200]
    }
    
    h_anuales = h_semanales * 44.2
    factor_j = h_semanales / 40
    anios = [2026, 2027, 2028, 2029] if "COMPLETO" in modo else [int(modo)]
    
    p_acumulado = p_actual

    for anio in anios:
        p_ant = p_acumulado
        m_ant = (p_ant * h_anuales) / pagas_anuales
        
        # Configuración de subidas según convenio
        fijo, unico = (1.04, 0.02) if anio == 2026 else (1.03, 0.015)
        inc_tramos = 1.03 ** (anio - 2026) if anio > 2026 else 1.0

        s_proyectado = p_acumulado * h_anuales
        s_con_fijo = s_proyectado * fijo
        
        n_salario, p_u, encontrado = 0, 0.0, False
        for t in tramos_base[categoria]:
            t_act = (t * inc_tramos) * factor_j
            if s_con_fijo < t_act:
                n_salario = t_act
                encontrado = True
                break
        
        if not encontrado:
            n_salario = s_con_fijo
            p_u = s_proyectado * (unico)
            
        p_acumulado = n_salario / h_anuales
        m_new = n_salario / pagas_anuales
        inc_anual = ((p_acumulado / p_ant) - 1) * 100

        # --- SALIDA VISUAL PROFESIONAL ---
        st.markdown(f"""
            <div class="card-resumen">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color:white; font-weight:bold; font-size:18px;">AÑO {anio}</span>
                    <span class="badge-inc">+{inc_anual:.2f}% Anual</span>
                </div>
                <div class="grid-comparativa">
                    <div class="data-box">
                        <p class="label-box">Precio Hora</p>
                        <span class="val-old">{p_ant:.2f} €/h</span>
                        <span class="val-new">{p_acumulado:.4f} €/h</span>
                    </div>
                    <div class="data-box">
                        <p class="label-box">Mensual Bruto ({pagas_anuales} pagas)</p>
                        <span class="val-old">{m_ant:,.2f} €</span>
                        <span class="val-new">{m_new:,.2f} €</span>
                    </div>
                </div>
                {f'<div class="pago-unico">💰 Pago Único Consolidado: {p_u:,.2f} €</div>' if p_u > 0 else ""}
            </div>
        """, unsafe_allow_html=True)
