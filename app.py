import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Convenio 2026-2029 Pro", layout="centered")

# Estilo Premium
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%); background-attachment: fixed; }
    .titulo { text-align: center; color: #f8fafc; font-size: 30px; font-weight: 800; text-transform: uppercase; margin-bottom: 20px; }
    .card-resumen {
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px; padding: 20px; margin-bottom: 15px; border-left: 8px solid #3b82f6;
    }
    .card-total { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 2px solid #10b981; border-radius: 20px; padding: 25px; text-align: center; margin-top: 30px; }
    .label-year { color: #3b82f6; font-size: 22px; font-weight: 900; margin-bottom: 5px; }
    .val-salario { color: white; font-size: 26px; font-weight: 700; }
    .val-pago { color: #f59e0b; font-size: 18px; font-weight: 600; }
    .stButton>button { width: 100%; height: 60px; border-radius: 15px !important; background: #2563eb !important; color: white !important; font-weight: 700 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">Simulador de Convenio 2026-2029</p>', unsafe_allow_html=True)

# --- SELECTOR DE MODO ---
modo = st.selectbox("📅 SELECCIONA PERIODO", ["Individual: 2026", "Individual: 2027", "Individual: 2028", "Individual: 2029", "COMPLETO (Resumen 4 años)"])

# --- ENTRADAS ---
col1, col2 = st.columns(2)
with col1:
    p_inicial = st.number_input("Precio Hora Actual (€)", value=10.0, format="%.2f")
    h_sem = st.number_input("Horas Semanales", value=40.0)
with col2:
    cat_act = st.selectbox("Categoría", ["Cajer@", "Asistent@", "Adjunt@", "Gt"])
    pagas = st.selectbox("Pagas", [12, 14])

btn = st.button("GENERAR PROYECCIÓN DE CONVENIO")

if btn:
    # Tramos base 2026
    tramos_base = {
        "Cajer@": [18800, 19800, 21000], "Asistent@": [21000, 22000, 23000],
        "Adjunt@": [25000, 27000, 29000], "Gt": [29500, 31000, 33600, 35000, 38200]
    }
    
    factor_j = h_sem / 40
    h_anuales = h_sem * 44.2
    
    # Lista de años a calcular
    anios_proyectar = [2026, 2027, 2028, 2029] if "COMPLETO" in modo else [int(modo.split(": ")[1])]
    
    p_corriente = p_inicial
    resumen_final = []

    for anio in anios_proyectar:
        # Configuración por año
        if anio == 2026:
            subida_fija = 1.04; subida_unica = 0.02; inc_tramos = 1.0
        else:
            subida_fija = 1.03; subida_unica = 0.015; inc_tramos = 1.03 ** (anio - 2026)

        s_proyectado = p_corriente * h_anuales
        s_con_fija = s_proyectado * subida_fija
        
        n_salario = 0; p_u = 0.0; encontrado = False
        
        for t in tramos_base[cat_act]:
            t_act = (t * inc_tramos) * factor_j
            if s_con_fija < t_act:
                n_salario = t_act
                encontrado = True
                break
        
        if not encontrado:
            n_salario = s_con_fija
            p_u = s_proyectado * subida_unica
            
        p_corriente = n_salario / h_anuales
        resumen_final.append({"anio": anio, "salario": n_salario, "precio_h": p_corriente, "pago_u": p_u})

    # --- SALIDA VISUAL ---
    if "COMPLETO" in modo:
        st.markdown('<p style="color:white; font-size:24px; font-weight:bold; text-align:center;">📋 RESUMEN DE VIGENCIA</p>', unsafe_allow_html=True)
        total_p_u = 0
        for r in resumen_final:
            total_p_u += r['pago_u']
            st.markdown(f"""
                <div class="card-resumen">
                    <p class="label-year">AÑO {r['anio']}</p>
                    <p class="val-salario">Salario: {r['salario']:,.0f}€ <span style="font-size:16px; color:#94a3b8;">({r['precio_h']:.2f}€/h)</span></p>
                    {"<p class='val-pago'>💰 Pago Único: " + str(round(r['pago_u'],2)) + "€</p>" if r['pago_u'] > 0 else ""}
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="card-total">
                <p style="color:#10b981; font-size:20px; font-weight:bold; text-transform:uppercase;">Balance Final 2029</p>
                <p style="color:white; font-size:32px; font-weight:900;">{resumen_final[-1]['precio_h']:.2f} €/hora</p>
                <p style="color:#94a3b8;">Mejora total: +{((resumen_final[-1]['precio_h']/p_inicial)-1)*100:.2f}%</p>
                <p style="color:#f59e0b; font-weight:bold;">Total Pagos Únicos: {total_p_u:,.2f}€</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Mostrar tarjeta individual (mismo estilo que antes)
        r = resumen_final[0]
        st.success(f"Cálculo para {r['anio']} finalizado. Precio hora: {r['precio_h']:.2f}€")
