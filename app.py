import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="Simulador Salarial 26-29", layout="centered")

# Estilo de Alto Contraste (Blanco sobre Negro/Azul)
st.markdown("""
    <style>
    .stApp { background: #0f172a; }
    .titulo { text-align: center; color: #ffffff; font-size: 26px; font-weight: 800; margin-bottom: 20px; }
    
    /* Etiquetas de inputs en BLANCO PURO para visibilidad en móvil */
    label { color: #ffffff !important; font-weight: 800 !important; font-size: 15px !important; }
    
    .card-anio {
        background: #1e293b; border: 1px solid #475569; border-radius: 14px;
        padding: 18px; margin-bottom: 20px;
    }
    .header-anio { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #475569; padding-bottom: 10px; }
    .badge-inc { background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: 700; }
    
    .grid-datos { display: flex; flex-direction: column; gap: 12px; }
    @media (min-width: 600px) {
        .grid-datos { flex-direction: row; justify-content: space-between; }
        .col-dato { flex: 1; }
    }
    
    .col-dato { background: #0f172a; padding: 12px; border-radius: 10px; border-left: 4px solid #3b82f6; }
    .label-dato { color: #94a3b8; font-size: 11px; text-transform: uppercase; font-weight: 700; margin-bottom: 4px; }
    .val-old { color: #cbd5e1; font-size: 14px; display: block; margin-bottom: 2px; }
    .val-new { color: #ffffff; font-size: 20px; font-weight: 800; display: block; }
    
    .pago-mano { background: rgba(245, 158, 11, 0.2); border: 1px dashed #f59e0b; color: #fbbf24; padding: 10px; border-radius: 8px; margin-top: 15px; text-align: center; font-weight: 800; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">📊 SIMULADOR CONVENIO 2026-2029</p>', unsafe_allow_html=True)

# --- PANEL DE ENTRADA ---
with st.expander("⚙️ CONFIGURACIÓN DE DATOS", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        p_actual_input = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
        h_sem_ant = st.number_input("Horas Semanales Actuales", value=40.0)
    with c2:
        h_sem_new = st.number_input("Horas Nuevo Convenio", value=40.0)
        n_pagas = st.selectbox("Número de Pagas", [12, 14, 15])
    
    cat = st.selectbox("Categoría Profesional", ["Cajer@/Reponedor", "Asistent@ / Oficial", "Adjunt@", "Gt"])
    vista = st.selectbox("Proyectar hasta el año:", ["2026", "2027", "2028", "2029", "COMPLETO"])

if st.button("🚀 CALCULAR EVOLUCIÓN"):
    # Tramos Base 2026
    tramos_base = {
        "Cajer@/Reponedor": [18800, 19800, 21000],
        "Asistent@ / Oficial": [21000, 22000, 23000],
        "Adjunt@": [25000, 27000, 29000],
        "Gt": [29500, 31000, 33600, 35000, 38200]
    }
    
    h_anuales_ant = h_sem_ant * 44.2
    h_anuales_new = h_sem_new * 44.2
    f_jornada_new = h_sem_new / 40
    
    limite = 2029 if vista == "COMPLETO" else int(vista)
    anios_rango = list(range(2026, limite + 1))
    
    p_acumulado = p_actual_input

    for anio in anios_rango:
        # Referencias previas
        h_ref = h_anuales_ant if anio == 2026 else h_anuales_new
        p_ant = p_acumulado
        a_ant = p_ant * h_ref
        m_ant = a_ant / n_pagas
        
        # Parámetros de subida según año
        fijo = 1.04 if anio == 2026 else 1.03
        mano_alzada_pct = 0.02 if anio == 2026 else 0.015
        
        # Actualizar último tramo (sube 3% anual acumulado desde 2026)
        tramos_anio = tramos_base[cat].copy()
        inc_ultimo_tramo = 1.03 ** (anio - 2026)
        tramos_anio[-1] = tramos_anio[-1] * inc_ultimo_tramo
        
        # Proyectamos subida en nómina
        salario_con_fijo = p_ant * h_anuales_new * fijo
        
        n_anual = 0
        p_u = 0.0
        excede_tramos = True
        
        # Buscamos si entra en tramos
        for t in tramos_anio:
            t_ajustado = t * f_jornada_new
            if salario_con_fijo < t_ajustado:
                n_anual = t_ajustado
                excede_tramos = False
                break
        
        # Lógica de rebase definitiva
        if excede_tramos:
            n_anual = salario_con_fijo
            p_u = a_ant * mano_alzada_pct # 2% o 1,5% sobre el bruto del año anterior
            
        p_acumulado = n_anual / h_anuales_new
        m_new = n_anual / n_pagas
        inc_anual = ((p_acumulado / p_ant) - 1) * 100

        # --- RENDERIZADO TARJETA ---
        st.markdown(f"""
            <div class="card-anio">
                <div class="header-anio">
                    <span style="color:white; font-size:19px; font-weight:800;">EJERCICIO {anio}</span>
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
                {f'<div class="pago-mano">💰 Pago a Mano Alzada ({mano_alzada_pct*100}%): {p_u:,.2f} €</div>' if p_u > 0 else ""}
            </div>
        """, unsafe_allow_html=True)
