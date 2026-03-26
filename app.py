import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Simulador Salarial 26-29", layout="centered")

# Estilo de Máximo Contraste para Móvil
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; }
    .titulo { text-align: center; color: #ffffff; font-size: 24px; font-weight: 800; margin-bottom: 20px; }
    
    /* Etiquetas de inputs en BLANCO PURO para visibilidad en móvil */
    label { color: #ffffff !important; font-weight: 800 !important; font-size: 15px !important; }
    
    .card-anio {
        background: #1e293b; border: 1px solid #475569; border-radius: 14px;
        padding: 18px; margin-bottom: 20px;
    }
    .header-anio { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #475569; padding-bottom: 10px; }
    .badge-inc { background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: 700; }
    
    .grid-datos { display: flex; flex-direction: column; gap: 10px; }
    @media (min-width: 600px) {
        .grid-datos { flex-direction: row; justify-content: space-between; }
        .col-dato { flex: 1; }
    }
    
    .col-dato { background: #0f172a; padding: 10px; border-radius: 8px; border-left: 4px solid #3b82f6; }
    .label-dato { color: #94a3b8; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .val-old { color: #cbd5e1; font-size: 13px; display: block; }
    .val-new { color: #ffffff; font-size: 19px; font-weight: 800; display: block; }
    
    .pago-mano { background: rgba(245, 158, 11, 0.2); border: 2px dashed #f59e0b; color: #fbbf24; padding: 12px; border-radius: 10px; margin-top: 15px; text-align: center; font-weight: 800; }
    
    .stButton>button { width: 100%; background-color: #2563eb !important; color: white !important; font-weight: bold !important; height: 50px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">📊 SIMULADOR CONVENIO 2026-2029</p>', unsafe_allow_html=True)

# --- PANEL DE ENTRADA ---
with st.expander("⚙️ CONFIGURACIÓN DE DATOS (Toca para editar)", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        p_act = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
        h_ant = st.number_input("Horas Semanales Actuales", value=40.0)
    with c2:
        h_new = st.number_input("Horas Nuevo Convenio", value=40.0)
        pagas = st.selectbox("Número de Pagas", [12, 14])
    
    cat = st.selectbox("Categoría Profesional", ["Cajer@/Reponedor", "Asistent@ / Oficial", "Adjunt@", "Gt"])
    vista = st.selectbox("Proyectar hasta el año:", ["2026", "2027", "2028", "2029", "COMPLETO"])

if st.button("🚀 CALCULAR PROYECCIÓN REAL"):
    # Tramos Base 2026
    tramos_base = {
        "Cajer@/Reponedor": [18800, 19800, 21000],
        "Asistent@ / Oficial": [21000, 22000, 23000],
        "Adjunt@": [25000, 27000, 29000],
        "Gt": [29500, 31000, 33600, 35000, 38200]
    }
    
    h_an_ant = h_ant * 44.2
    h_an_new = h_new * 44.2
    f_jornada = h_new / 40
    
    limite = 2029 if vista == "COMPLETO" else int(vista)
    anios_rango = list(range(2026, limite + 1))
    
    p_acumulado = p_act

    for anio in anios_rango:
        # Valores año anterior
        h_ref_prev = h_an_ant if anio == 2026 else h_an_new
        p_prev = p_acumulado
        a_prev = p_prev * h_ref_prev
        m_prev = a_prev / pagas
        
        # Parámetros subida anual
        pct_nomina = 1.04 if anio == 2026 else 1.03
        pct_mano_alzada = 0.02 if anio == 2026 else 0.015
        
        # Tramos: El último sube 3% anual acumulado desde 2026
        tramos_anio = tramos_base[cat].copy()
        inc_ultimo = 1.03 ** (anio - 2026)
        tramos_anio[-1] = tramos_anio[-1] * inc_ultimo
        ultimo_tramo_limite = tramos_anio[-1] * f_jornada
        
        # Salario proyectado con subida fija en nueva jornada
        salario_proyectado = (p_prev * h_an_new) * pct_nomina
        
        n_anual = 0
        p_u = 0.0
        
        # REGLA DE REBASE (Específica para Adjuntos y topes de tabla)
        # Si el salario ya está en el último tramo o lo supera tras aplicar la subida
        if salario_proyectado >= (ultimo_tramo_limite - 0.01):
            n_anual = salario_proyectado
            p_u = a_prev * pct_mano_alzada
        else:
            # Buscar si cae en algún tramo intermedio
            encontrado = False
            for t in tramos_anio:
                t_ajustado = t * f_jornada
                if salario_proyectado < t_ajustado:
                    n_anual = t_ajustado
                    encontrado = True
                    break
            if not encontrado:
                n_anual = salario_proyectado
                p_u = a_prev * pct_mano_alzada

        p_acumulado = n_anual / h_an_new
        m_new = n_anual / pagas
        inc_anual = ((p_acumulado / p_prev) - 1) * 100

        # --- SALIDA VISUAL ---
        st.markdown(f"""
            <div class="card-anio">
                <div class="header-anio">
                    <span style="color:white; font-size:18px; font-weight:800;">EJERCICIO {anio}</span>
                    <span class="badge-inc">+{inc_anual:.2f}% Nómina</span>
                </div>
                <div class="grid-datos">
                    <div class="col-dato">
                        <p class="label-dato">Precio Hora</p>
                        <span class="val-old">Antes: {p_prev:.2f} €</span>
                        <span class="val-new">{p_acumulado:.2f} €</span>
                    </div>
                    <div class="col-dato">
                        <p class="label-dato">Mensual ({pagas} pagas)</p>
                        <span class="val-old">Antes: {m_prev:,.2f} €</span>
                        <span class="val-new">{m_new:,.2f} €</span>
                    </div>
                    <div class="col-dato">
                        <p class="label-dato">Bruto Anual</p>
                        <span class="val-old">Antes: {a_prev:,.2f} €</span>
                        <span class="val-new">{n_anual:,.2f} €</span>
                    </div>
                </div>
                {f'<div class="pago-mano">💰 PAGO A MANO ALZADA ({round(pct_mano_alzada*100, 1)}%): {p_u:,.2f} €</div>' if p_u > 0 else ""}
            </div>
        """, unsafe_allow_html=True)
