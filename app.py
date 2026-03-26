import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Revisión UGT-LIDL Pro", layout="wide")

# URLs de logos (asegúrate de que funcionen o cámbialas por las reales)
url_ugt_bg = "https://wikimedia.org"
url_lidl_logo = "https://wikimedia.org"

# 2. Estilo CSS
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.9)), 
                    url("{url_ugt_bg}");
        background-size: 600px; background-position: center; background-repeat: no-repeat; background-attachment: fixed;
    }}
    .lidl-corner {{ position: fixed; top: 15px; left: 15px; width: 85px; z-index: 999; }}
    .titulo {{ text-align: center; color: #3B82F6; font-size: 48px; font-weight: 900; margin-top: 10px; }}
    .ahi-lo-llevas {{ text-align: center; color: #FACC15; font-size: 45px; font-weight: 900; margin: 20px 0; text-transform: uppercase; }}
    .expediente {{
        text-align: center; color: white; background: rgba(30, 41, 59, 0.95);
        padding: 25px; border-radius: 20px; font-size: 34px; font-weight: bold;
        border: 4px solid #3B82F6; margin: 25px 0;
    }}
    .card {{
        background: rgba(30, 41, 59, 0.95); border-radius: 25px; padding: 35px;
        border-left: 15px solid #3B82F6; margin-bottom: 30px;
    }}
    .res-label {{ color: #94A3B8; font-size: 20px; font-weight: bold; text-transform: uppercase; }}
    .res-valor {{ color: #F8FAFC; font-size: 38px; font-weight: 900; line-height: 1.2; }}
    .res-extra {{ color: #10B981; font-size: 24px; font-weight: bold; margin-top: 5px; }}
    
    .stNumberInput label, .stSelectbox label, .stTextInput label {{
        color: white !important; font-size: 26px !important; font-weight: bold !important;
    }}
    input, div[data-baseweb="select"] {{ font-size: 24px !important; height: 65px !important; }}
    .stButton>button {{ height: 80px; font-size: 26px !important; font-weight: bold !important; background: linear-gradient(90deg, #10B981 0%, #059669 100%) !important; border-radius: 15px !important; }}
    </style>
    <img src="{url_lidl_logo}" class="lidl-corner">
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">REVISIÓN SALARIAL</p>', unsafe_allow_html=True)

# --- DATOS DE ENTRADA ---
col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.markdown('<p style="color:#3B82F6; font-size:28px; font-weight:bold;">📥 DATOS DE ENTRADA</p>', unsafe_allow_html=True)
    p_ant = st.number_input("Precio Hora Año Pasado (€)", min_value=0.0, value=10.0, format="%.2f")
    h_ant = st.number_input("Horas Sem. Año Pasado", min_value=0.0, max_value=40.0, value=40.0)
    h_act = st.number_input("Horas Sem. Actuales", min_value=0.0, max_value=40.0, value=40.0)
    cat_act = st.selectbox("Categoría Actual", ["Cajer@", "Asistent@", "Adjunt@", "Gt"])
    pagas = st.selectbox("Número de Pagas", [12, 14])
    
    btn = st.button("🚀 CALCULAR AHORA", use_container_width=True)

with col_out:
    st.markdown('<p style="color:#10B981; font-size:28px; font-weight:bold;">📊 RESULTADOS</p>', unsafe_allow_html=True)
    
    if btn:
        # LÓGICA DE NEGOCIO
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
        
        # Comparativa: qué cobraría hoy con su precio antiguo pero jornada nueva
        s_base_proyectado = p_ant * h_an_act
        s_con_4_fijo = s_base_proyectado * 1.04
        
        n_salario_anual = 0
        pago_unico = 0.0
        encontrado = False
        
        # Buscamos en tramos
        for t in tramos_base[cat_act]:
            t_prop = t * factor_act
            if s_con_4_fijo < t_prop:
                n_salario_anual = t_prop
                encontrado = True
                break
        
        # SI SUPERA EL ÚLTIMO TRAMO: 4% consolidado y 2% pago único
        if not encontrado:
            n_salario_anual = s_con_4_fijo
            pago_unico = s_base_proyectado * 0.02
            
        p_nue = n_salario_anual / h_an_act
        mensual_nue = n_salario_anual / pagas
        pct_subida = ((p_nue / p_ant) - 1) * 100
        dif_mensual = mensual_nue - mensual_ant

        # --- SALIDA VISUAL ---
        st.markdown('<p class="ahi-lo-llevas">¡AHÍ LO LLEVAS! 🚀</p>', unsafe_allow_html=True)

        # 1. PRECIO HORA
        st.markdown(f"""
            <div class="card">
                <p class="res-label">Precio Hora</p>
                <p class="res-valor">{p_ant:.2f}€ ➔ {p_nue:.2f}€</p>
                <p class="res-extra">Incremento: +{pct_subida:.2f}%</p>
            </div>
        """, unsafe_allow_html=True)

        # 2. PAGO ÚNICO (Si existe)
        if pago_unico > 0:
            st.markdown(f"""
                <div class="card" style="border-left-color:#F59E0B">
                    <p class="res-label">Pago Único (2% Extra)</p>
                    <p class="res-valor">{pago_unico:,.2f}€</p>
                    <p style="color:#F8FAFC; font-size:16px;">No consolidable (pago de una sola vez).</p>
                </div>
            """, unsafe_allow_html=True)

        # 3. MENSUALIDAD
        st.markdown(f"""
            <div class="card" style="border-left-color:#10B981">
                <p class="res-label">Sueldo Mensual Bruto ({pagas} Pagas)</p>
                <p class="res-valor">{mensual_ant:,.2f}€ ➔ {mensual_nue:,.2f}€</p>
                <p class="res-extra">Diferencia: +{dif_mensual:.2f}€/mes</p>
            </div>
        """, unsafe_allow_html=True)

        # 4. ANUAL
        st.markdown(f"""
            <div class="card" style="border-left-color:#A78BFA">
                <p class="res-label">Salario Anual Bruto</p>
                <p class="res-valor">{salario_an_ant:,.0f}€ ➔ {n_salario_anual:,.0f}€</p>
            </div>
        """, unsafe_allow_html=True)
