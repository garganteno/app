import streamlit as st

# Configuración de página
st.set_page_config(page_title="Simulador Salarial Pro", layout="centered")

# Estilo de Alto Contraste para Móvil
st.markdown("""
    <style>
    .stApp { background: #0a0f1e; }
    .titulo { text-align: center; color: #ffffff; font-size: 24px; font-weight: 800; margin-bottom: 20px; }
    label { color: #ffffff !important; font-weight: 800 !important; font-size: 15px !important; }
    .card-anio {
        background: #1e293b; border: 1px solid #475569; border-radius: 14px;
        padding: 18px; margin-bottom: 20px;
    }
    .header-anio { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #475569; padding-bottom: 10px; }
    .badge-inc { background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: 700; }
    .grid-datos { display: flex; flex-direction: column; gap: 10px; }
    @media (min-width: 600px) { .grid-datos { flex-direction: row; justify-content: space-between; } .col-dato { flex: 1; } }
    .col-dato { background: #0f172a; padding: 10px; border-radius: 8px; border-left: 4px solid #3b82f6; }
    .label-dato { color: #94a3b8; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .val-old { color: #cbd5e1; font-size: 13px; display: block; }
    .val-new { color: #ffffff; font-size: 19px; font-weight: 800; display: block; }
    .pago-mano { background: rgba(245, 158, 11, 0.2); border: 2px dashed #f59e0b; color: #fbbf24; padding: 12px; border-radius: 10px; margin-top: 15px; text-align: center; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="titulo">📊 CONVENIO 2026-2029 (ÚLTIMO TRAMO)</p>', unsafe_allow_html=True)

with st.expander("⚙️ DATOS DE ENTRADA", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        p_act = st.number_input("Precio Hora Actual (€)", value=10.00, format="%.2f")
        h_ant = st.number_input("Horas Semanales Actuales", value=40.0)
    with c2:
        h_new = st.number_input("Horas Nuevo Convenio", value=40.0)
        pagas = st.selectbox("Pagas", [12, 14])
    cat = st.selectbox("Categoría", ["Cajer@/Reponedor", "Asistent@ / Oficial", "Adjunt@", "Gt"])
    vista = st.selectbox("Proyectar hasta:", ["2026", "2027", "2028", "2029", "COMPLETO"])

if st.button("🚀 CALCULAR CON REBASE REAL"):
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
    anios = list(range(2026, limite + 1))
    
    p_acum = p_act

    for anio in anios:
        # Valores del año anterior para cálculos
        h_ref_ant = h_an_ant if anio == 2026 else h_an_new
        p_prev = p_acum
        a_prev = p_prev * h_ref_ant
        m_prev = a_prev / pagas
        
        # Parámetros del año actual
        fijo = 1.04 if anio == 2026 else 1.03
        mano_alzada = 0.02 if anio == 2026 else 0.015
        
        # Tramos del año actual: Solo el último sube el 3% anual acumulado
        tramos_anio = tramos_base[cat].copy()
        inc_ultimo = 1.03 ** (anio - 2026)
        tramos_anio[-1] = tramos_anio[-1] * inc_ultimo
        ultimo_tramo_ajustado = tramos_anio[-1] * f_jornada
        
        n_anual = 0
        p_u = 0.0

        # LÓGICA DE REBASE MEJORADA:
        # Si el salario actual (ajustado a la nueva jornada) ya es >= al último tramo
        salario_actual_en_nueva_jornada = p_prev * h_an_new
        
        if salario_actual_en_nueva_jornada >= ultimo_tramo_ajustado:
            # REBASE DIRECTO: Sube el % en nómina y cobra el % a mano alzada
            n_anual = salario_actual_en_nueva_jornada * fijo
            p_u = a_prev * mano_alzada
        else:
            # Búsqueda de tramos o subida fija
            subida_fija_proyectada = salario_actual_en_nueva_jornada * fijo
            
            if subida_fija_proyectada >= ultimo_tramo_ajustado:
                # Si la subida le hace saltar al último tramo o superarlo
                n_anual = subida_fija_proyectada
                p_u = a_prev * mano_alzada
            else:
                # Buscar tramo intermedio
                encontrado = False
                for t in tramos_anio:
                    t_aj = t * f_jornada
                    if subida_fija_proyectada < t_aj:
                        n_anual = t_aj
                        encontrado = True
                        break
                if not encontrado: n_anual = subida_fija_proyectada

        p_acum = n_anual / h_an_new
        m_new = n_anual / pagas
        inc_anual = ((p_acum / p_prev) - 1) * 100

        # Renderizado
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
                        <span class="val-new">{p_acum:.2f} €</span>
                    </div>
                    <div class="col-dato">
                        <p class="label-dato">Mensual ({pagas} pagas)</p>
                        <span class="val-old">Antes: {m_prev:,.2f} €</span>
                        <span class="val-new">{m_new:,.2f} €</span>
                    </div>
                    <div class="col-dato">
                        <p class="label-dato">Anual Bruto</p>
                        <span class="val-old">Antes: {a_prev:,.2f} €</span>
                        <span class="val-new">{n_anual:,.2f} €</span>
                    </div>
                </div>
                {f'<div class="pago-mano">💰 PAGO A MANO ALZADA ({int(mano_alzada*100)}% + {fijo*100-100}% Nómina): {p_u:,.2f} €</div>' if p_u > 0 else ""}
            </div>
        """, unsafe_allow_html=True)
