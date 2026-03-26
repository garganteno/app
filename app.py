import streamlit as st

# 1. Configuración de la página
st.set_page_config(page_title="Calculadora Salarial", layout="wide")

# 2. Estilo CSS (Simplificado y Directo)
st.markdown("""
    <style>
    .stApp { background-color: #0F172A; }
    .titulo-principal { text-align: center; color: #3B82F6; font-size: 40px; font-weight: 900; margin-bottom: 30px; }
    
    .ahi-lo-llevas { 
        text-align: center; color: #FACC15; font-size: 48px; 
        font-weight: 900; margin: 20px 0px; text-transform: uppercase;
    }
    
    .card-res { background-color: #1E293B; border-radius: 20px; padding: 30px; border-left: 10px solid #3B82F6; margin-bottom: 20px; }
    .card-green { border-left: 10px solid #10B981; }
    .card-purple { border-left: 10px solid #A78BFA; }
    .card-orange { border-left: 10px solid #F59E0B; }
    
    .label-card { color: #94A3B8; font-size: 18px; font-weight: bold; }
    .val-card { color: #F8FAFC; font-size: 34px; font-weight: 900; }
    
    .stNumberInput label, .stSelectbox label { color: #FFFFFF !important; font-size: 20px !important; font-weight: bold !important; }
    input { font-size: 20px !important; height: 50px !important; }
    
    .stButton>button { 
        height: 80px; font-size: 26px !important; font-weight: bold !important; 
        background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important; 
        border-radius: 15px !important; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo-principal">REVISIÓN SALARIAL</p>', unsafe_allow_html=True)

# --- ENTRADA DE DATOS ---
col_in, col_spacer, col_out = st.columns([1, 0.1, 1.2])

with col_in:
    p_ant = st.number_input("Precio Hora Año Pasado (€)", min_value=0.0, value=10.0, format="%.2f", step=0.1)
    h_ant = st.number_input("Horas Semanales Año Pasado", min_value=0.0, max_value=40.0, value=40.0)
    h_act = st.number_input("Horas Semanales Actuales", min_value=0.0, max_value=40.0, value=40.0)
    cat_act = st.selectbox("Categoría Actual", ["Cajer@", "Asistent@", "Adjunt@", "Gt"])
    pagas = st.selectbox("Número de Pagas", [12, 14])
    
    st.write("---")
    btn_calcular = st.button("🚀 CALCULAR")

# --- LÓGICA Y RESULTADOS ---
if btn_calcular:
    # 1. Bases
    h_anuales_ant = h_ant * 44.2
    s_anual_ant = p_ant * h_anuales_ant
    mensual_ant = s_anual_ant / pagas
    
    tramos = {
        "Cajer@": [18800, 19800, 21000], 
        "Asistent@": [21000, 22000, 23000], 
        "Adjunt@": [25000, 27000, 29000], 
        "Gt": [29500, 31000, 33600, 35000, 38200]
    }
    
    factor_jornada = h_act / 40
    h_anuales_act = h_act * 44.2
    
    # Proyectamos el sueldo actual a la nueva jornada + 4%
    s_proyectado_nuevo = (p_ant * h_anuales_act)
    s_base_con_4 = s_proyectado_nuevo * 1.04
    
    n_salario_anual = 0
    pago_unico = 0.0
    
    # 2. Comprobar Tramos
    ultimo_tramo = tramos[cat_act][-1] * factor_jornada
    
    for t in tramos[cat_act]:
        t_prop = t * factor_jornada
        if s_base_con_4 < t_prop:
            n_salario_anual = t_prop
            break
            
    # 3. Si supera el último tramo: 4% consolidado y 2% pago único
    if n_salario_anual == 0:
        n_salario_anual = s_base_con_4
        pago_unico = s_proyectado_nuevo * 0.02
    
    # 4. Finales
    p_nuevo = n_salario_anual / h_anuales_act
    mensual_nue = n_salario_anual / pagas
    dif_m = mensual_nue - mensual_ant

    with col_out:
        st.markdown('<p class="ahi-lo-llevas">¡AHÍ LO LLEVAS! 🚀</p>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="card-res">
                <p class="label-card">NUEVO PRECIO HORA</p>
                <p class="val-card">{p_ant:.2f}€ ➔ {p_nuevo:.2f}€</p>
            </div>
        """, unsafe_allow_html=True)

        if pago_unico > 0:
            st.markdown(f"""
                <div class="card-res card-orange">
                    <p class="label-card">PAGO ÚNICO (Extra 2%)</p>
                    <p class="val-card">{pago_unico:,.2f}€</p>
                    <p style="color:#F8FAFC; font-size:14px;">Dinero extra (No va al sueldo mensual)</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="card-res card-purple">
                <p class="label-card">SALARIO ANUAL BRUTO</p>
                <p class="val-card">{n_salario_anual:,.0f}€</p>
            </div>
            <div class="card-res card-green">
                <p class="label-card">MENSUAL ({pagas} PAGAS)</p>
                <p class="val-card">{mensual_nue:,.2f}€</p>
                <p style="color:#10B981; font-weight:bold;">Subida: +{dif_m:,.2f}€/mes</p>
            </div>
        """, unsafe_allow_html=True)
