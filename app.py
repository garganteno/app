import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Revisión Salarial Pro", layout="centered")

# URLs de logos (puedes cambiarlas por las definitivas)
url_ugt_bg = "https://wikimedia.org"
url_lidl_logo = "https://wikimedia.org"

# 2. Estilo CSS PROFESIONAL
st.markdown(f"""
    <style>
    /* Fondo con degradado profundo */
    .stApp {{
        background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%);
        background-attachment: fixed;
    }}
    
    .lidl-corner {{ position: fixed; top: 15px; left: 15px; width: 65px; z-index: 999; filter: drop-shadow(0 2px 5px rgba(0,0,0,0.5)); }}
    
    .titulo {{ 
        text-align: center; color: #f8fafc; font-size: 32px; font-weight: 800; 
        letter-spacing: -1px; margin-bottom: 30px; text-transform: uppercase;
    }}

    /* Tarjeta de resultados con efecto cristal */
    .card-pro {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 25px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }}
    
    .card-highlight {{ border-left: 6px solid #3b82f6; }}
    .card-success {{ border-left: 6px solid #10b981; }}
    .card-warning {{ border-left: 6px solid #f59e0b; background: rgba(245, 158, 11, 0.05); }}

    .label-pro {{ color: #94a3b8; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
    .valor-pro {{ color: #ffffff; font-size: 38px; font-weight: 800; margin: 5px 0; }}
    .sub-valor {{ color: #10b981; font-size: 18px; font-weight: 600; }}
    
    .ahi-lo-llevas {{ 
        text-align: center; color: #fbbf24; font-size: 40px; font-weight: 900; 
        margin: 20px 0; letter-spacing: -2px; line-height: 1;
    }}

    /* Inputs elegantes */
    .stNumberInput label, .stSelectbox label {{ color: #cbd5e1 !important; font-weight: 600 !important; }}
    input {{ border-radius: 12px !important; background: #1e293b !important; color: white !important; border: 1px solid #334155 !important; }}
    
    /* Botón Premium */
    .stButton>button {{
        width: 100%; height: 65px; border-radius: 16px !important;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important; font-weight: 700 !important; font-size: 20px !important;
        border: none !important; box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3) !important;
    }}
    </style>
    <img src="{url_lidl_logo}" class="lidl-corner">
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">Panel de Revisión</p>', unsafe_allow_html=True)

# Contenedor de Entradas
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        p_ant = st.number_input("Precio Hora Ant.", value=10.0, format="%.2f")
        h_ant = st.number_input("Horas Sem. Ant.", value=40.0)
    with col2:
        h_act = st.number_input("Horas Sem. Act.", value=40.0)
        pagas = st.selectbox("Pagas", [12, 14])
    
    cat_act = st.selectbox("Categoría", ["Cajer@", "Asistent@", "Adjunt@", "Gt"])
    st.write("")
    btn = st.button("CALCULAR INCREMENTO")

if btn:
    # --- LÓGICA (Mantenemos la regla 4%+2%) ---
    h_an_ant = h_ant * 44.2
    salario_an_ant = p_ant * h_an_ant
    mensual_ant = salario_an_ant / pagas
    
    tramos_base = {"Cajer@": [18800, 19800, 21000], "Asistent@": [21000, 22000, 23000], 
                   "Adjunt@": [25000, 27000, 29000], "Gt": [29500, 31000, 33600, 35000, 38200]}
    
    factor_act = h_act / 40
    h_an_act = h_act * 44.2
    s_proyectado = p_ant * h_an_act
    s_con_4 = s_proyectado * 1.04
    
    n_salario = 0
    pago_unico = 0.0
    encontrado = False
    
    for t in tramos_base[cat_act]:
        t_p = t * factor_act
        if s_con_4 < t_p:
            n_salario = t_p
            encontrado = True
            break
    
    if not encontrado:
        n_salario = s_con_4
        pago_unico = s_proyectado * 0.02
        
    p_nue = n_salario / h_an_act
    mensual_nue = n_salario / pagas
    pct = ((p_nue / p_ant) - 1) * 100

    # --- SALIDA PROFESIONAL ---
    st.markdown('<p class="ahi-lo-llevas">¡AHÍ LO LLEVAS! 🚀</p>', unsafe_allow_html=True)

    # Fila 1: Precio Hora
    st.markdown(f"""
        <div class="card-pro card-highlight">
            <p class="label-pro">Valor de tu Hora</p>
            <p class="valor-pro">{p_nue:.2f}<span style="font-size:20px"> €</span></p>
            <p class="sub-valor">Anterior: {p_ant:.2f}€ | <span style="color:#fbbf24">+{pct:.2f}%</span></p>
        </div>
    """, unsafe_allow_html=True)

    # Pago Único (Solo si aplica)
    if pago_unico > 0:
        st.markdown(f"""
            <div class="card-pro card-warning">
                <p class="label-pro">Pago Único Extraord.</p>
                <p class="valor-pro" style="color:#f59e0b">{pago_unico:,.2f}€</p>
                <p style="color:#94a3b8; font-size:14px; font-weight:600;">(2% No consolidable en nómina)</p>
            </div>
        """, unsafe_allow_html=True)

    # Fila 2: Mensualidad
    st.markdown(f"""
        <div class="card-pro card-success">
            <p class="label-pro">Nuevo Bruto Mensual</p>
            <p class="valor-pro">{mensual_nue:,.2f}€</p>
            <p class="sub-valor">Sube: +{mensual_nue - mensual_ant:.2f}€ / mes</p>
        </div>
    """, unsafe_allow_html=True)

    # Fila 3: Anual
    st.markdown(f"""
        <div class="card-pro">
            <p class="label-pro">Salario Anual Bruto</p>
            <p class="valor-pro" style="font-size:28px">{n_salario:,.0f}€</p>
            <p style="color:#64748b; font-size:14px;">Antes: {salario_an_ant:,.0f}€</p>
        </div>
    """, unsafe_allow_html=True)
