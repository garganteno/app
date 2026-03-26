import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Evolución Salarial 26-29", layout="wide")

# Estilo Profesional Refinado
st.markdown("""
    <style>
    .stApp { background: #0f172a; }
    .titulo { text-align: center; color: #f8fafc; font-size: 28px; font-weight: 800; margin-bottom: 25px; }
    .card-anio {
        background: #1e293b; border: 1px solid #334155; border-radius: 12px;
        padding: 20px; margin-bottom: 20px;
    }
    .header-anio { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 10px; margin-bottom: 15px; }
    .badge-inc { background: #10b981; color: white; padding: 4px 12px; border-radius: 6px; font-size: 14px; font-weight: 700; }
    
    .grid-datos { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; }
    .col-dato { background: #0f172a; padding: 12px; border-radius: 8px; border-left: 4px solid #3b82f6; }
    .label-dato { color: #94a3b8; font-size: 11px; text-transform: uppercase; font-weight: 600; margin-bottom: 4px; }
    .val-old { color: #94a3b8; font-size: 14px; display: block; margin-bottom: 2px; }
    .val-new { color: #ffffff; font-size: 22px; font-weight: 700; display: block; }
    
    .pago-extra { background: rgba(245, 158, 11, 0.1); border: 1px solid #f59e0b; color: #fbbf24; padding: 8px; border-radius: 6px; margin-top: 15px; text-align: center; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">📈 EVOLUCIÓN SALARIAL CONVENIO 2026-2029</p>', unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
with st.sidebar:
    st.header("Configuración")
    p_actual_input = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
    h_sem = st.number_input("Horas Semanales", value=40.0)
    cat = st.selectbox("Categoría", ["Cajer@/Reponedor", "Asistent@ / Oficial", "Adjunt@", "Gt"])
    n_pagas = st.selectbox("Pagas", [12, 14])
    vista = st.selectbox("Ver hasta el año:", ["2026", "2027", "2028", "2029", "COMPLETO"])

if st.button("GENERAR INFORME DE EVOLUCIÓN"):
    # Tramos Base 2026
    tramos_base = {
        "Cajer@/Reponedor": [18800, 19800, 21000],
        "Asistent@ / Oficial": [21000, 22000, 23000],
        "Adjunt@": [25000, 27000, 29000],
        "Gt": [29500, 31000, 33600, 35000, 38200]
    }
    
    h_anuales = h_sem * 44.2
    f_jornada = h_sem / 40
    limite = 2029 if vista == "COMPLETO" else int(vista)
    anios_rango = list(range(2026, limite + 1))
    
    p_acumulado = p_actual_input

    for anio in anios_rango:
        p_ant = p_acumulado
        m_ant = (p_ant * h_anuales) / n_pagas
        a_ant = p_ant * h_anuales
        
        # Subidas según año
        fijo = 1.04 if anio == 2026 else 1.03
        unico = 0.02 if anio == 2026 else 0.015
        
        salario_base_calculo = p_acumulado * h_anuales
        salario_con_fijo = salario_base_calculo * fijo
        
        # Ajuste de tramos: Solo el último sube el 3% anual acumulado
        tramos_anio = tramos_base[cat].copy()
        inc_ultimo_tramo = 1.03 ** (anio - 2026)
        tramos_anio[-1] = tramos_anio[-1] * inc_ultimo_tramo
        
        n_anual, p_u, encontrado = 0, 0.0, False
        for t in tramos_anio:
            t_ajustado = t * f_jornada
            if salario_con_fijo < t_ajustado:
                n_anual = t_ajustado
                encontrado = True
                break
        
        if not encontrado:
            n_anual = salario_con_fijo
            p_u = salario_base_calculo * unico
            
        p_acumulado = n_anual / h_anuales
        m_new = n_anual / n_pagas
        inc_anual = ((p_acumulado / p_ant) - 1) * 100

        # --- SALIDA VISUAL ---
        st.markdown(f"""
            <div class="card-anio">
                <div class="header-anio">
                    <span style="color:white; font-size:20px; font-weight:800;">EJERCICIO {anio}</span>
                    <span class="badge-inc">+{inc_anual:.2f}% Incremento</span>
                </div>
                <div class="grid-datos">
                    <div class="col-dato">
                        <p class="label-dato">Precio Hora</p>
                        <span class="val-old">Anterior: {p_ant:.2f} €</span>
                        <span class="val-new">{p_acumulado:.2f} €/h</span>
                    </div>
                    <div class="col-dato">
                        <p class="label-dato">Salario Mensual ({n_pagas} pagas)</p>
                        <span class="val-old">Anterior: {m_ant:,.2f} €</span>
                        <span class="val-new">{m_new:,.2f} €</span>
                    </div>
                    <div class="col-dato">
                        <p class="label-dato">Salario Bruto Anual</p>
                        <span class="val-old">Anterior: {a_ant:,.2f} €</span>
                        <span class="val-new">{n_anual:,.2f} €</span>
                    </div>
                </div>
                {f'<div class="pago-extra">💰 Pago Único por Convenio: {p_u:,.2f} €</div>' if p_u > 0 else ""}
            </div>
        """, unsafe_allow_html=True)
