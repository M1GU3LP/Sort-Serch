import streamlit as st
import random
import time

# ══════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════
st.set_page_config(page_title="Sort & Search Feria", page_icon="📊")

# Estilos personalizados para emular tu diseño oscuro
st.markdown("""
    <style>
    .main { background-color: #0d121f; color: #edf2f7; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    div[data-testid="stMetricValue"] { color: #2ed1a2; }
    </style>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# ALGORITMOS (Tu lógica original)
# ══════════════════════════════════════════════

def orden_burbuja(lista):
    lst = lista[:]
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst

def orden_insercion(lista):
    lst = lista[:]
    for i in range(1, len(lst)):
        val = lst[i]
        j = i
        while j > 0 and lst[j - 1] > val:
            lst[j] = lst[j - 1]
            j -= 1
        lst[j] = val
    return lst

def _mezcla(iz, de):
    l, i, j = [], 0, 0
    while i < len(iz) and j < len(de):
        if iz[i] < de[j]:
            l.append(iz[i]); i += 1
        else:
            l.append(de[j]); j += 1
    l.extend(iz[i:])
    l.extend(de[j:])
    return l

def orden_mezcla(lista):
    if len(lista) <= 1:
        return lista[:]
    mid = len(lista) // 2
    return _mezcla(orden_mezcla(lista[:mid]), orden_mezcla(lista[mid:]))

def busqueda_lineal(lista, ob):
    for i, e in enumerate(lista):
        if e == ob: return i
    return -1

def busqueda_binaria(lista, ob):
    l, r = 0, len(lista) - 1
    while l <= r:
        mid = (l + r) // 2
        if lista[mid] == ob: return mid
        elif ob > lista[mid]: l = mid + 1
        else: r = mid - 1
    return -1

# ══════════════════════════════════════════════
# INTERFAZ STREAMLIT
# ══════════════════════════════════════════════

st.title("📊 SORT & SEARCH")
st.caption("Ordenamiento · Búsqueda · Tiempo Real")

# Inicializar estado de la lista
if 'lista_base' not in st.session_state:
    numbers = [str(i).zfill(4) for i in range(10000)]
    random.shuffle(numbers)
    st.session_state.lista_base = numbers
    st.session_state.lista_ordenada = None

# 1. Entrada de datos
st.subheader("1. Configura tu objetivo")
objetivo = st.text_input("Ingresa el número a buscar (4 dígitos):", 
                         max_chars=4, placeholder="Ej: 1234",type="password")

if objetivo:
    if not objetivo.isdigit() or len(objetivo) != 4:
        st.error("Escribe exactamente 4 dígitos (0000-9999)")
    else:
        # 2. Selección de Ordenamiento
        st.divider()
        st.subheader("2. Elige el algoritmo de ordenamiento")
        col1, col2, col3 = st.columns(3)
        
        algo_ord = None
        with col1: 
            if st.button("Burbuja"): algo_ord = (orden_burbuja, "Burbuja")
        with col2: 
            if st.button("Inserción"): algo_ord = (orden_insercion, "Inserción")
        with col3: 
            if st.button("Mezcla"): algo_ord = (orden_mezcla, "Mezcla")

        if algo_ord:
            fn, nombre = algo_ord
            t0 = time.perf_counter()
            st.session_state.lista_ordenada = fn(st.session_state.lista_base)
            t1 = time.perf_counter()
            st.session_state.t_orden = (t1 - t0) * 1_000_000
            st.session_state.nombre_orden = nombre
            st.success(f"¡{nombre} completado!")

        # 3. Selección de Búsqueda (Solo si ya se ordenó)
        if st.session_state.lista_ordenada:
            st.divider()
            st.subheader("3. Elige el algoritmo de búsqueda")
            c_b1, c_b2 = st.columns(2)
            
            algo_busq = None
            with c_b1:
                if st.button("Lineal"): algo_busq = (busqueda_lineal, "Lineal")
            with c_b2:
                if st.button("Binaria"): algo_busq = (busqueda_binaria, "Binaria")

            if algo_busq:
                fn_b, nombre_b = algo_busq
                t0_b = time.perf_counter()
                idx = fn_b(st.session_state.lista_ordenada, objetivo)
                t1_b = time.perf_counter()
                
                # ══════════════════════════════════════════════
                # RESUMEN FINAL
                # ══════════════════════════════════════════════
                st.divider()
                st.header("🏆 Resumen Final")
                
                m1, m2 = st.columns(2)
                m1.metric("Ordenamiento", st.session_state.nombre_orden)
                m1.write(f"⏱️ {st.session_state.t_orden:,.1f} μs")
                
                m2.metric("Búsqueda", nombre_b)
                t_busq = (t1_b - t0_b) * 1_000_000
                m2.write(f"⏱️ {t_busq:,.1f} μs")

                if idx >= 0:
                    st.balloons()
                    st.info(f"🎯 **Encontrado:** {objetivo} en la posición {idx + 1}")
                else:
                    st.error(f"❌ **No encontrado:** {objetivo}")
                
                if st.button("Reiniciar"):
                    st.session_state.clear()
                    st.rerun()