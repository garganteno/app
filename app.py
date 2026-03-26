import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Simulador Salarial 26-29", layout="centered")

# Estilo Profesional / Corporate Dark
st.markdown("""
    <style>
    .stApp { background: #0f172a; }
    .titulo { text-align: center; color: #f8fafc; font-size: 32px; font-weight: 800; margin-bottom: 30px; letter-spacing: -1px; }
    
    /* Tarjeta Principal */
    .card-resumen {
        background: #1e293b; border: 1px solid #334155; border-radius: 16px;
        padding: 24px; margin-bottom: 20px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    .badge-year { background: #3b82f6; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: 700; }
    .badge-inc { background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: 700; }
    
    /* Comparativas */
    .grid-comparativa { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }
    .data-box { background: #0f172a; padding: 15px; border-radius: 12px; border: 1px solid #1e293b; }
    .label-box { color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; }
    
    .val-old { color: #64748b; font-size: 14px; text-decoration: line-through; display: block; }
    .val-new { color: #f8fafc; font-size: 22px; font-weight: 700; display: block; }
    .sub-new { color: #10b981; font-size: 12px; font-weight: 600; }
    
    .pago-unico { background: rgba(245, 158, 11, 0.1); border: 1px dashed #f59e0b; color: #fbbf24; 
                  padding: 10px; border-radius: 8px; margin-top: 15px; text-align: center; font-weight: 600; }
    
    hr { border: 0; border-top: 1px solid #334155; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">📊 Proyección de Convenio 2026 - 2029</p>', unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
with st.sidebar:
    st.header("Configuración")
    p_actual = st.number_input("Precio Hora Actual (€)", value=10.0, step=0.1, format="%.2f")
    h_semanales = st.number_input("Horas Semanales", value=40.0, step=1.0)
    categoria = st.selectbox("Categoría Profesional", ["Cajer@/Reponedor", "Asistent@ / Oficial", "Adjunt@", "Gt"])
    pagas_anuales = st.radio("Número de Pagas", [12, 14], horizontal=True)
    periodo = st.selectbox("Vista de Datos", ["Resumen Completo (4 años)", "Solo 2026", "Solo 2027", "Solo 2028", "Solo 2029"])

# --- LÓGICA DE CÁLCULO ---
if st.sidebar.button("CALCULAR INCREMENTOS"):
    tramos = {
        "Cajer@/Reponedor": [18800, 19800, 21000],
        "Asistent@ / Oficial": [21000, 22000, 23000],
        "Adjunt@": [25000, 27000, 29000],
        "Gt": [29500, 31000, 33600, 35000, 38200]
    }
    
    h_anuales = h_semanales * 44.2 # Coeficiente según convenio estándar
    factor_jornada = h_semanales / 40
    
    anios = [2026, 2027, 2028, 2029]
    if "202" in periodo: anios = [int(periodo.split()[-1])]
    
    p_hora_base = p_actual
    
    for anio in anios:
        # Variables de control anual
        p_anterior = p_hora_base
        m_anterior = (p_anterior * h_anuales) / pagas_anuales
        
        # Parámetros del convenio
        if anio == 2026:
            fijo, unico, inc_t = 1.04, 0.02, 1.0
        else:
            fijo, unico, inc_t = 1.03, 0.015, (1.03**(anio-2026))

        # Cálculo de subida
        salario_proyectado = p_hora_base * h_anuales
        salario_con_fijo = salario_proyectado * fijo
        
        pago_u = 0.0
        encontrado = False
        for t in tramos[categoria]:
            t_ajustado = (t * inc_t) * factor_jornada
            if salario_con_fija < t_ajustado:
                nuevo_salario_anual = t_ajustado
                encontrado = True
                break
        
        if not encontrado:
            nuevo_salario_anual = salario_con_fijo
            pago_u = salario_proyectado * unico
            
        p_hora_base = nuevo_salario_anual / h_anuales
        m_nuevo = nuevo_salario_anual / pagas_anuales
        inc_porcentual = ((p_hora_base / p_anterior) - 1) * 100

        # --- RENDERIZADO DE TARJETA PROFESIONAL ---
        st.markdown(f"""
            <div class="card-resumen">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="badge-year">EJERCICIO {anio}</span>
                    <span class="badge-inc">+{inc_porcentual:.2f}% Incremento Anual</span>
                </div>
                
                <div class="grid-comparativa">
                    <div class="data-box">
                        <p class="label-box">Precio Hora (€/h)</p>
                        <span class="val-old">{p_anterior:.2f} €</span>
                        <span class="val-new">{p_hora_base:.4f} €</span>
                        <span class="sub-new">Diferencia: +{(p_hora_base - p_anterior):.2f}€</span>
                    </div>
                    <div class="data-box">
                        <p class="label-box">Mensual Bruto ({pagas_anuales} pagas)</p>
                        <span class="val-old">{m_anterior:,.2f} €</span>
                        <span class="val-new">{m_nuevo:,.2f} €</span>
                        <span class="sub-new">Anual: {(nuevo_salario_anual):,.0f}€</span>
                    </div>
                </div>
                
                {f'<div class="pago-unico">🎁 Pago Único Consolidado: {pago_u:,.2f} €</div>' if pago_u > 0 else ""}
            </div>
        """, unsafe_allow_html=True)

else:
    st.info("Configura los datos en el panel izquierdo y pulsa 'Calcular Incrementos'.")
