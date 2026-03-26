import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Revisión Salarial Centrada", layout="centered")

# URLs de logos
url_ugt_bg = "https://wikimedia.org"
url_lidl_logo = "https://wikimedia.org"

# 2. Estilo CSS para CENTRAR TODO
st.markdown(f"""
    <style>
    /* Fondo y centrado general */
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.95)), 
                    url("{url_ugt_bg}");
        background-size: 500px; background-position: center; background-repeat: no-repeat; background-attachment: fixed;
    }}
    
    /* Contenedor para limitar el ancho y centrar */
    .main-container {{
        max-width: 700px;
        margin: 0 auto;
    }}

    .lidl-corner {{ position: fixed; top: 15px; left: 15px; width: 70px; z-index: 999; }}
    .titulo {{ text-align: center; color: #3B82F6; font-size: 42px; font-weight: 900; margin-top: 10px; text-transform: uppercase; }}
    .ahi-lo-llevas {{ text-align: center; color: #FACC15; font-size: 45px; font-weight: 900; margin: 25px 0; text-shadow: 2px 2px 10px rgba(250, 204, 21, 0.3); }}
    
    /* Tarjetas */
    .card {{
        background: rgba(30, 41, 59, 0.95); border-radius: 20px; padding: 25px;
        border-left: 10px solid #3B82F6; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .res-label {{ color: #94A3B8; font-size: 18px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }}
    .res-valor {{ color: #F8FAFC; font-size: 34px; font-weight: 900; }}
    .res-extra {{ color: #10B981; font-size: 20px; font-weight: bold; }}

    /* Inputs */
    .stNumberInput label, .stSelectbox label {{
        color: white !important; font-size: 22px !important; font-weight: bold !important;
    }}
    input {{ font-size: 20px !important; height: 55px !important; text-align: center; }}
    
    /* Botón */
    .stButton>button {{
        height: 70px; font-size: 24px !important; font-weight: bold !important;
        background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important;
        border-radius: 15px !important; border: none !important; color: white !important;
    }}
    </style>
    <img src="{url_lidl_logo}" class="lidl-corner">
    """, unsafe_allow_html=True)

# Encabezado
st.markdown('<p class="titulo">REVISIÓN SALARIAL</p>', unsafe_allow_html=True)

# Usamos una sola columna central para que no se vea vacío a los lados
col_central = st.columns([1, 10, 1])[1]

with col_central:
    st.markdown('<p style="color:#3B82F6; font-size:24px; font-weight:bold; text-align:center;">📥 DATOS DEL TRABAJADOR</p>', unsafe_allow_html=True)
    p_ant = st.number_input("Precio Hora Año Pasado (€)", min_value=0.0, value=10.0, format="%.2f")
    
    c1, c2 = st.columns(2)
    with c1:
        h_ant = st.number_input("Horas Sem. Ant.", min_value=0.0, max_value=40.0, value=40.0)
    with c2:
        h_act = st.number_input("Horas Sem. Act.", min_value=0.0, max_value=40.0, value=40.0)
    
    cat_act = st.selectbox("Categoría Actual", ["Cajer@", "Asistent@", "Adjunt@", "Gt"])
    pagas = st.selectbox("Número de Pagas", [12, 14])
    
    st.write("")
    btn = st.button("🚀 CALCULAR AHORA", use_container_width=True)

    if btn:
        # LÓGICA DE CÁLCULO
        h_an_ant = h_ant * 44.2
        salario_an_ant = p_ant * h_an_ant
        mensual_ant = salario_an_ant / pagas
        
        tramos_base = {
            "Cajer@": [18800, 19800, 21000],
            "Asistent@": [21000, 22000, 23000],
            "Adjunt@": [25000, 27000, 29000],
            "Gt": [29500, 31000, 33600, 35000, 38200]
        }
        
        factor_act = h_act / 40
        h_an_act = h_act * 44.2
        s_base_proyectado = p_ant * h_an_act
        s_con_4_fijo = s_base_proyectado * 1.04
        
        n_salario_anual = 0
        pago_unico = 0.0
        encontrado = False
        
        for t in tramos_base[cat_act]:
            t_prop = t * factor_act
            if s_con_4_fijo < t_prop:
                n_salario_anual = t_prop
                encontrado = True
                break
        
        if not encontrado:
            n_salario_anual = s_con_4_fijo
            pago_unico = s_base_proyectado * 0.02
            
        p_nue = n_salario_anual / h_an_act
        mensual_nue = n_salario_anual / pagas
        pct_subida = ((p_nue / p_ant) - 1) * 100
        dif_mensual = mensual_nue - mensual_ant

        # --- RESULTADOS CENTRADOS ---
        st.markdown('<p class="ahi-lo-llevas">¡AHÍ LO LLEVAS! 🚀</p>', unsafe_allow_html=True)

        st.markdown(f"""
            <div class="card">
                <p class="res-label">PRECIO HORA</p>
                <p class="res-valor">{p_ant:.2f}€ ➔ {p_nue:.2f}€</p>
                <p class="res-extra">Subida: +{pct_subida:.2f}%</p>
            </div>
        """, unsafe_allow_html=True)

        if pago_unico > 0:
            st.markdown(f"""
                <div class="card" style="border-left-color:#F59E0B">
                    <p class="res-label">PAGO ÚNICO (2% Extra)</p>
                    <p class="res-valor">{pago_unico:,.2f}€</p>
                    <p style="color:#F8FAFC; font-size:14px;">Pago extraordinario (No consolidable)</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="card" style="border-left-color:#10B981">
                <p class="res-label">MENSUALIDAD ({pagas} PAGAS)</p>
                <p class="res-valor">{mensual_ant:,.2f}€ ➔ {mensual_nue:,.2f}€</p>
                <p class="res-extra">Diferencia: +{dif_mensual:.2f}€/mes</p>
            </div>
            <div class="card" style="border-left-color:#A78BFA">
                <p class="res-label">SALARIO ANUAL BRUTO</p>
                <p class="res-valor">{salario_an_ant:,.0f}€ ➔ {n_salario_anual:,.0f}€</p>
            </div>
        """, unsafe_allow_html=True)
