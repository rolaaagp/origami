import streamlit as st
import pandas as pd
import re
import json
from io import BytesIO
from datetime import datetime
import unicodedata
import hashlib


# Cache para las funciones de transformación
@st.cache_resource
def get_acciones():
    """Retorna el diccionario de acciones cacheado"""
    return build_acciones()

@st.cache_resource
def get_categorias():
    """Retorna las categorías de funciones cacheadas"""
    return build_categorias()


def limpiar_rut(v):
    return re.sub(r'[^0-9kK]', '', str(v)).upper() if pd.notna(v) else ""


def formatear_rut(v):
    if len(str(v)) <= 1:
        return v
    return f"{int(str(v)[:-1]):,}-{str(v)[-1]}".replace(",", ".")


def fecha_latam(v):
    try:
        return pd.to_datetime(v).strftime('%d-%m-%Y')
    except:
        return v


def fecha_iso(v):
    try:
        return pd.to_datetime(v).strftime('%Y-%m-%d')
    except:
        return ""


def capitalizar_todo(v):
    return str(v).upper() if pd.notna(v) else ""


def minusculas_todo(v):
    return str(v).lower() if pd.notna(v) else ""


def titulo_propio(v):
    return str(v).title() if pd.notna(v) else ""


def limpiar_extremos(v):
    return str(v).strip() if pd.notna(v) else ""


def solo_letras(v):
    return re.sub(r'[^a-zA-Z\s]', '', str(v))


def solo_numeros(v):
    return re.sub(r'[^0-9]', '', str(v)) if pd.notna(v) else ""


def a_entero(v):
    try:
        return int(float(v))
    except:
        return 0


def a_decimal(v):
    try:
        return round(float(v), 2)
    except:
        return 0.0


def formato_contable(v):
    try:
        return f"$ {float(v):,.0f}".replace(",", ".")
    except:
        return "$ 0"


def extraer_anio(v):
    try:
        return pd.to_datetime(v).year
    except:
        return ""


def extraer_mes(v):
    try:
        return pd.to_datetime(v).month
    except:
        return ""


def nombre_dia(v):
    try:
        return pd.to_datetime(v).day_name(locale='es_ES')
    except:
        return ""


def reemplazar_nulos_cero(v):
    return 0 if pd.isna(v) else v


def reemplazar_nulos_vacio(v):
    return "" if pd.isna(v) else v


def anonimizar_correo(v):
    if pd.isna(v) or '@' not in str(v):
        return "xxx@xxx.com"
    parte_nom, dominio = str(v).split('@')
    return f"{parte_nom[0]}***@{dominio}"


def eliminar_tildes(v):
    if pd.notna(v):
        return "".join(c for c in unicodedata.normalize('NFD', str(v)) if unicodedata.category(c) != 'Mn')
    return ""


def solo_alfanumerico(v):
    return re.sub(r'[^a-zA-Z0-9]', '', str(v))


def primera_palabra(v):
    if pd.notna(v) and len(str(v).split()) > 0:
        return str(v).split()[0]
    return ""


def ultima_palabra(v):
    if pd.notna(v) and len(str(v).split()) > 0:
        return str(v).split()[-1]
    return ""


def longitud_caracteres(v):
    return len(str(v)) if pd.notna(v) else 0


def es_numerico(v):
    return "SI" if str(v).replace('.', '').isdigit() else "NO"


def email_valido(v):
    return "VÁLIDO" if '@' in str(v) and '.' in str(v) else "INVÁLIDO"


def contar_palabras(v):
    return len(str(v).split()) if pd.notna(v) else 0


def calcular_iva(v):
    try:
        return round(float(v) * 0.19, 2)
    except:
        return 0


def neto_desde_bruto(v):
    try:
        return round(float(v) / 1.19, 2)
    except:
        return 0


def categorizar_monto(v):
    try:
        val = float(v)
        if val < 100000:
            return "Bajo"
        if val < 1000000:
            return "Medio"
        return "Alto"
    except:
        return "N/A"


def porcentaje_de_100(v):
    try:
        return f"{(float(v)/100):.1%}"
    except:
        return "0%"


def limpiar_telefono(v):
    nums = re.sub(r'[^0-9]', '', str(v))
    if len(nums) == 9:
        return f"+56{nums}"
    return nums


def extraer_dominio(v):
    if pd.isna(v) or '@' not in str(v):
        return ""
    return str(v).split('@')[-1]


def crear_username(v):
    if pd.notna(v):
        return "".join([w[0] for w in str(v).split()]).lower()
    return ""


def dias_hasta_hoy(v):
    try:
        diff = datetime.now() - pd.to_datetime(v)
        return diff.days
    except:
        return 0


def semestre_anio(v):
    try:
        return f"S{(pd.to_datetime(v).month-1)//6 + 1}"
    except:
        return ""


def trimestre(v):
    try:
        return f"Q{(pd.to_datetime(v).month-1)//3 + 1}"
    except:
        return ""


def es_fin_semana(v):
    try:
        return "SI" if pd.to_datetime(v).weekday() >= 5 else "NO"
    except:
        return ""


def id_unico(v):
    return f"{v}-{datetime.now().strftime('%f')[:3]}"


def rellenar_ceros(v):
    return str(v).zfill(8) if pd.notna(v) else ""

# --- LÓGICA DE NEGOCIO Y FINANZAS ---


def calcular_edad(v):
    try:
        nacimiento = pd.to_datetime(v)
        hoy = datetime.now()
        return hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
    except:
        return ""


def cuotas_estimadas(v, n_cuotas=12):
    try:
        return round(float(v) / n_cuotas, 0)
    except:
        return 0


def hash_sensible(v):
    if pd.isna(v):
        return ""
    return hashlib.sha256(str(v).encode()).hexdigest()[:12]


def extraer_solo_texto(v):
    return re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', str(v))


def nivel_riesgo_monto(v):
    try:
        val = float(v)
        if val > 5000000:
            return "CRÍTICO (Requiere Aprobación)"
        if val > 1000000:
            return "ALTO"
        return "NORMAL"
    except:
        return "DESCONOCIDO"


def aplicar_formula_libre(fila, formula, columnas_disponibles):
    try:
        patron = r'\[([^\]]+)\]'

        def sustituir_variable(match):
            nombre_col = match.group(1)
            if nombre_col in columnas_disponibles:
                valor = fila[nombre_col]
                if pd.isna(valor):
                    return "0"
                if isinstance(valor, str):
                    return f"'{valor}'"
                return str(valor)
            return "0"

        f_preparada = re.sub(patron, sustituir_variable, formula)
        partes = f_preparada.split('+')
        resultados_partes = []

        for parte in partes:
            res_segmento = eval(parte.strip())
            resultados_partes.append(str(res_segmento))

        return " ".join(resultados_partes)

    except Exception as e:
        return f"Error en fórmula: {str(e)}"


def build_acciones():
    """Construye el diccionario de acciones"""
    return {
        "Copia Directa": None,
        "Fórmula Libre / Combinar": "FORMULA",
        "RUT: Limpiar (12.345.678-9 -> 123456789)": limpiar_rut,
        "RUT: Formatear (123456789 -> 12.345.678-9)": formatear_rut,
        "Texto: Todo MAYÚSCULAS": capitalizar_todo,
        "Texto: todo minúsculas": minusculas_todo,
    "Texto: Formato Nombre Propio": titulo_propio,
    "Texto: Eliminar espacios extra": limpiar_extremos,
    "Texto: Solo letras (A-Z)": solo_letras,
    "Números: Solo Dígitos": solo_numeros,
    "Números: Convertir a Entero": a_entero,
    "Números: Convertir a Decimal (2 dec)": a_decimal,
    "Números: Formato Contable ($)": formato_contable,
    "Fecha: DD-MM-AAAA": fecha_latam,
    "Fecha: AAAA-MM-DD (ISO)": fecha_iso,
    "Fecha: Solo Año": extraer_anio,
    "Fecha: Solo Mes (Número)": extraer_mes,
    "Fecha: Nombre del Día (ES)": nombre_dia,
    "Limpieza: Reemplazar Nulos por 0": reemplazar_nulos_cero,
    "Limpieza: Reemplazar Nulos por 'Vacío'": reemplazar_nulos_vacio,
    "Privacidad: Anonimizar Email": anonimizar_correo,
    "Texto: Eliminar Tildes": eliminar_tildes,
    "Texto: Solo caracteres Alfanuméricos": solo_alfanumerico,
    "Texto: Primera palabra": primera_palabra,
    "Texto: Última palabra": ultima_palabra,
    "Auditoría: Longitud de caracteres": longitud_caracteres,
    "Auditoría: ¿Es Numérico? (SI/NO)": es_numerico,
    "Auditoría: ¿Tiene @? (Email Válido)": email_valido,
    "Auditoría: Contar palabras": contar_palabras,
    "Finanzas: Calcular IVA (19%)": calcular_iva,
    "Finanzas: Neto desde Bruto": neto_desde_bruto,
    "Finanzas: Categorizar Monto (Bajo/Medio/Alto)": categorizar_monto,
    "Finanzas: Porcentaje de 100 (v/100)": porcentaje_de_100,
    "Contacto: Formato Teléfono Chile (+56)": limpiar_telefono,
    "Contacto: Extraer Dominio de Email": extraer_dominio,
    "Contacto: Crear Nombre de Usuario (sigla)": crear_username,
    "Tiempo: Días transcurridos hasta hoy": dias_hasta_hoy,
    "Tiempo: Semestre del Año": semestre_anio,
    "Tiempo: Trimestre (Q1, Q2...)": trimestre,
    "Tiempo: ¿Es Fin de Semana? (SI/NO)": es_fin_semana,
    "Especial: ID Único Aleatorio": id_unico,
    "Especial: Rellenar con ceros (8 dígitos)": rellenar_ceros,
    # --- CATEGORÍA: RECURSOS HUMANOS ---
    "RRHH: Calcular Edad (desde fecha)": calcular_edad,
    "RRHH: Iniciales (Juan Perez -> J.P.)": lambda v: ".".join([w[0] for w in str(v).split()]).upper() + "." if pd.notna(v) else "",
    "RRHH: Género Sugerido (por nombre)": lambda v: "F" if str(v).strip().lower().endswith(('a', 'ia', 'na')) else "M",

    # --- CATEGORÍA: FINANZAS PRO ---
    "Finanzas: Cuota mensual (12 meses s/int)": lambda v: cuotas_estimadas(v, 12),
    "Finanzas: Cuota mensual (24 meses s/int)": lambda v: cuotas_estimadas(v, 24),
    "Finanzas: Nivel de Riesgo (por Monto)": nivel_riesgo_monto,
    "Finanzas: ¿Monto es Par o Impar?": lambda v: "PAR" if int(float(v)) % 2 == 0 else "IMPAR" if pd.notna(v) else "",
    # --- CATEGORÍA: LOGÍSTICA Y UBICACIÓN ---
    "Geo: Pais Predeterminado (Chile)": lambda v: "Chile",
    "Geo: Región sugerida (desde Ciudad)": lambda v: "Metropolitana" if "santiago" in str(v).lower() else "Otras Regiones",
    "Logística: Formato Código de Barras (EAN13)": lambda v: str(v).zfill(13),

    # --- CATEGORÍA: DATA CLEANSING AVANZADO ---
    "Limpieza: Solo Texto (sin números/símbolos)": extraer_solo_texto,
    "Limpieza: Remover saltos de línea": lambda v: str(v).replace('\n', ' ').replace('\r', ''),
    "Limpieza: Capitalizar cada palabra": lambda v: " ".join([w.capitalize() for w in str(v).split()]),
    "Limpieza: Eliminar ceros a la izquierda": lambda v: str(v).lstrip('0'),

    # --- CATEGORÍA: CIBERSEGURIDAD (GDPR) ---
    "Seguridad: Enmascarar RUT (XXXXX-X)": lambda v: "XXXXX-" + str(v)[-1] if len(str(v)) > 1 else "X",
    "Seguridad: Hash SHA256 (ID único oculto)": hash_sensible,
    "Seguridad: Ocultar Teléfono (****1234)": lambda v: "*" * (len(str(v))-4) + str(v)[-4:] if len(str(v)) > 4 else v,

    # --- CATEGORÍA: ESTADÍSTICA RÁPIDA ---
    "Datos: ¿Es mayor de edad? (SI/NO)": lambda v: "SI" if calcular_edad(v) >= 18 else "NO",
    "Datos: Longitud sin espacios": lambda v: len(str(v).replace(" ", "")),
    "Datos: Invertir texto (Espejo)": lambda v: str(v)[::-1],
    }
    return acciones

# ═══════════════════════════════════════════════════════════════════════════
#  ORGANIZACIÓN DE FUNCIONES POR CATEGORÍA
# ═══════════════════════════════════════════════════════════════════════════
def build_categorias():
    """Construye las categorías de funciones"""
    acciones = get_acciones()
    return {
        "Basico": ["Copia Directa", "Fórmula Libre / Combinar"],
        "Texto": [k for k in acciones.keys() if "Texto:" in k or "texto" in k.lower()],
        "Números": [k for k in acciones.keys() if "Números:" in k or "números" in k.lower()],
        "Fechas": [k for k in acciones.keys() if "Fecha:" in k or "Tiempo:" in k],
        "RUT/ID": [k for k in acciones.keys() if "RUT:" in k or "Identidad" in k],
        "Contacto": [k for k in acciones.keys() if "Contacto:" in k],
        "Finanzas": [k for k in acciones.keys() if "Finanzas:" in k],
        "Limpieza": [k for k in acciones.keys() if "Limpieza:" in k or "Limpieza" in k],
        "Seguridad": [k for k in acciones.keys() if "Seguridad:" in k],
        "Auditoría": [k for k in acciones.keys() if "Auditoría:" in k],
        "RRHH": [k for k in acciones.keys() if "RRHH:" in k],
        "Datos": [k for k in acciones.keys() if "Datos:" in k],
    }

# Inicializar ACCIONES y CATEGORIAS_FUNCIONES con cache
ACCIONES = get_acciones()
CATEGORIAS_FUNCIONES = get_categorias()


st.set_page_config(
    page_title="Origami - Transformación de Datos",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════
# PERSONALIZACIÓN VISUAL
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
    <style>
    /* Header Principal */
    .main-header {
        padding: 20px 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
        color: white;
    }
    .main-title {
        font-size: 2.8em;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .sub-title {
        font-size: 1.1em;
        opacity: 0.95;
        margin: 8px 0 0 0;
    }
    
    /* Cards y Contenedores */
    .config-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border: 2px solid #e1e8ed;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    .config-card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        border-color: #667eea;
    }
    
    /* Badges y Tags */
    .function-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        margin: 4px;
    }
    .category-badge {
        background: #764ba2;
    }
    .warning-badge {
        background: #f59e0b;
    }
    .success-badge {
        background: #10b981;
    }
    
    /* Métrica Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
    }
    .metric-number {
        font-size: 2.5em;
        font-weight: 800;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 0.95em;
        opacity: 0.9;
    }
    
    /* Botones */
    .action-button {
        transition: all 0.3s ease;
    }
    
    /* Dividers */
    .divider-fancy {
        background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
        height: 2px;
        margin: 30px 0;
    }
    </style>
""", unsafe_allow_html=True)
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("Gestión de Plantillas")
    st.info("Guarda o carga configuraciones de mapeo para ahorrar tiempo.")
    archivo_plantilla = st.file_uploader(
        "Cargar Plantilla (.json)", type=["json"])

    st.markdown("<div class='divider-fancy'></div>", unsafe_allow_html=True)

    st.header("Categorías de Funciones")

    categorias = {
        "🔤 Texto": ["Mayúsculas", "minúsculas", "Nombre", "espacios", "letras"],
        "💰 Números": ["Dígitos", "Entero", "Decimal", "Contable"],
        "📅 Fechas": ["DD-MM-AAAA", "ISO", "Año", "Mes", "Día"],
        "🆔 Identidad": ["RUT", "Email", "Teléfono", "Usuario"],
        "💵 Finanzas": ["IVA", "Bruto", "Monto", "Riesgo"],
        "🛡️ Privacidad": ["Nulos", "Anonimizar", "Hash", "Enmascarar"],
    }

    for cat, items in categorias.items():
        with st.expander(cat, expanded=False):
            for item in items[:4]:
                st.caption(f"✓ {item}")

with st.expander("1. Entrada de Datos", expanded=True):
    col_up1, col_up2 = st.columns([2, 1])
    with col_up1:
        archivo = st.file_uploader(
            "Subir Excel/CSV de Origen", type=["xlsx", "csv"])
    with col_up2:
        st.info("Soporta Excel (.xlsx) y CSV")

# Resetear mapeo si el archivo fue removido
if not archivo and 'mapeo_lista' in st.session_state:
    del st.session_state.mapeo_lista
    if 'opciones_agrupadas_cache' in st.session_state:
        del st.session_state.opciones_agrupadas_cache

if archivo:
    if archivo.name.endswith('.csv'):
        df_orig = pd.read_csv(archivo)
    else:
        df_orig = pd.read_excel(archivo)

    cols_orig = df_orig.columns.tolist()

    if 'mapeo_lista' not in st.session_state:
        if archivo_plantilla:
            st.session_state.mapeo_lista = json.load(archivo_plantilla)
        else:
            st.session_state.mapeo_lista = [
                {"dest": c, "orig": c, "func": "Copia Directa", "formula": ""}
                for c in cols_orig
            ]

    # 🔍 BUSCADOR DE FUNCIONES
    st.markdown("<div class='divider-fancy'></div>", unsafe_allow_html=True)
    st.subheader("Búsqueda Rápida de Funciones")

    col_search, col_cat = st.columns([3, 1])
    with col_search:
        termino_busqueda = st.text_input(
            "Buscar transformación...",
            placeholder="Ej: RUT, Email, Fecha, IVA, etc.",
            key="search_func"
        )

    if termino_busqueda:
        funciones_encontradas = [
            f for f in ACCIONES.keys()
            if termino_busqueda.lower() in f.lower()
        ]

        if funciones_encontradas:
            st.success(f"Encontradas {len(funciones_encontradas)} funciones")
            cols_display = st.columns(min(3, len(funciones_encontradas)))
            for idx, func in enumerate(funciones_encontradas[:9]):
                with cols_display[idx % 3]:
                    st.markdown(
                        f"<span class='function-badge'>{func}</span>", unsafe_allow_html=True)
        else:
            st.warning("No se encontraron funciones con ese término")

    st.markdown("<div class='divider-fancy'></div>", unsafe_allow_html=True)
    st.subheader("2. Configuración de Mapeo")

    col_acc_1, col_acc_2, col_help = st.columns([1, 1, 2])

    if col_acc_1.button("+ Nueva Columna"):
        st.session_state.mapeo_lista.append({
            "dest": "",
            "orig": "(Vacío)",
            "func": "Copia Directa",
            "formula": ""
        })
        st.rerun()

    if col_acc_2.button("Resetear"):
        del st.session_state.mapeo_lista
        st.rerun()

    with col_help:
        st.info("""
            **Cómo usar:**
            1. Define el nombre de la columna destino
            2. Selecciona la columna origen
            3. Elige la transformación a aplicar
            4. Procesa para ver el resultado
        """)

    # Cache para opciones agrupadas (se calcula una sola vez)
    if 'opciones_agrupadas_cache' not in st.session_state:
        opciones_agrupadas_cache = []
        for cat, funcs in CATEGORIAS_FUNCIONES.items():
            if funcs:
                opciones_agrupadas_cache.append(cat)
                opciones_agrupadas_cache.extend(funcs)
        st.session_state.opciones_agrupadas_cache = opciones_agrupadas_cache

    opciones_agrupadas = st.session_state.opciones_agrupadas_cache

    # Cache para opciones agrupadas (se calcula una sola vez)
    if 'opciones_agrupadas_cache' not in st.session_state:
        opciones_agrupadas_cache = []
        for cat, funcs in CATEGORIAS_FUNCIONES.items():
            if funcs:
                opciones_agrupadas_cache.append(cat)
                opciones_agrupadas_cache.extend(funcs)
        st.session_state.opciones_agrupadas_cache = opciones_agrupadas_cache

    opciones_agrupadas = st.session_state.opciones_agrupadas_cache

    mapeo_actualizado = []

    for i, item in enumerate(st.session_state.mapeo_lista):
        c1, c2, c3, c4, c5 = st.columns([1.2, 1.5, 3.5, 2, 0.4])

        with c1:
            n_dest = st.text_input(
                "Destino",
                value=item['dest'],
                key=f"d_{i}",
                label_visibility="collapsed",
                placeholder="Columna"
            )

        with c2:
            indice_orig = 0
            if item['orig'] in cols_orig:
                indice_orig = cols_orig.index(item['orig']) + 1

            o_sel = st.selectbox(
                "Origen",
                ["(Vacío)"] + cols_orig,
                index=indice_orig,
                key=f"o_{i}",
                label_visibility="collapsed"
            )

        with c3:
            try:
                indice_func = opciones_agrupadas.index(item['func'])
            except:
                indice_func = opciones_agrupadas.index("Copia Directa") if "Copia Directa" in opciones_agrupadas else 0

            f_sel = st.selectbox(
                "Acción",
                opciones_agrupadas,
                index=indice_func,
                key=f"f_{i}",
                label_visibility="collapsed"
            )

        with c4:
            if f_sel == "Fórmula Libre / Combinar":
                formula = st.text_input(
                    "Fórmula",
                    value=item.get('formula', ''),
                    key=f"form_{i}",
                    label_visibility="collapsed",
                    placeholder="[Col1]+[Col2]"
                )
            elif f_sel == "Datos: ¿Es mayor de edad? (SI/NO)":
                edad_min = st.number_input(
                    "Edad",
                    value=int(item.get('formula', '18')) if item.get('formula') else 18,
                    min_value=0,
                    max_value=150,
                    key=f"form_{i}",
                    label_visibility="collapsed"
                )
                formula = str(edad_min)
            else:
                st.text("")
                formula = ""

        with c5:
            if st.button("X", key=f"del_{i}", use_container_width=True):
                st.session_state.mapeo_lista.pop(i)
                st.rerun()

        mapeo_actualizado.append({
            "dest": n_dest,
            "orig": o_sel,
            "func": f_sel,
            "formula": formula
        })

    st.session_state.mapeo_lista = mapeo_actualizado

    st.divider()

    col_exec, col_temp = st.columns([1, 1])

    with col_exec:
        if st.button("PROCESAR Y VISTA PREVIA"):
            df_dest = pd.DataFrame()

            for m in st.session_state.mapeo_lista:
                if not m['dest']:
                    continue

                if m['func'] == "Fórmula Libre / Combinar":
                    df_dest[m['dest']] = df_orig.apply(
                        lambda row: aplicar_formula_libre(
                            row, m['formula'], cols_orig),
                        axis=1
                    )
                elif m['func'] == "Datos: ¿Es mayor de edad? (SI/NO)":
                    # Usar la edad mínima del fórmula
                    edad_minima = int(m.get('formula', '18'))
                    df_dest[m['dest']] = df_orig[m['orig']].apply(
                        lambda v: "SI" if calcular_edad(v) >= edad_minima else "NO"
                    )
                elif m['orig'] != "(Vacío)":
                    func = ACCIONES[m['func']]
                    if func:
                        df_dest[m['dest']] = df_orig[m['orig']].apply(func)
                    else:
                        df_dest[m['dest']] = df_orig[m['orig']]
                else:
                    df_dest[m['dest']] = ""

            st.session_state.df_final = df_dest

            #  DASHBOARD DE RESUMEN
            st.markdown("<div class='divider-fancy'></div>",
                        unsafe_allow_html=True)
            st.subheader("Resumen de Procesamiento")

            # Métricas principales
            col_met1, col_met2, col_met3, col_met4 = st.columns(4)

            with col_met1:
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-label'>Filas Procesadas</div>
                        <div class='metric-number'>{len(df_dest)}</div>
                    </div>
                """, unsafe_allow_html=True)

            with col_met2:
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-label'>Columnas Creadas</div>
                        <div class='metric-number'>{len(df_dest.columns)}</div>
                    </div>
                """, unsafe_allow_html=True)

            with col_met3:
                nulos_totales = df_dest.isnull().sum().sum()
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-label'>Valores Nulos</div>
                        <div class='metric-number'>{nulos_totales}</div>
                    </div>
                """, unsafe_allow_html=True)

            with col_met4:
                tamaño_mb = df_dest.memory_usage(deep=True).sum() / 1024**2
                st.markdown(f"""
                    <div class='metric-card'>
                        <div class='metric-label'>Tamaño Datos</div>
                        <div class='metric-number'>{tamaño_mb:.2f} MB</div>
                    </div>
                """, unsafe_allow_html=True)

            # Detalles por columna
            st.markdown("<div class='divider-fancy'></div>",
                        unsafe_allow_html=True)
            st.subheader("Detalle de Columnas")

            col_info1, col_info2 = st.columns(2)

            with col_info1:
                st.write("**Columnas Creadas:**")
                for col in df_dest.columns:
                    nulos = df_dest[col].isnull().sum()
                    tipo = str(df_dest[col].dtype)
                    estado = "OK" if nulos == 0 else "REVISAR"
                    st.caption(f"{estado} `{col}` ({tipo}) - {nulos} nulos")

            with col_info2:
                st.write("**Configuración Aplicada:**")
                for m in st.session_state.mapeo_lista:
                    if m['dest']:
                        st.caption(
                            f"`{m['dest']}` <- `{m['orig']}` ({m['func'].split()[0]})")

            st.markdown("<div class='divider-fancy'></div>",
                        unsafe_allow_html=True)
            st.success("Transformación completada exitosamente")
            st.dataframe(df_dest.head(10), use_container_width=True)

    with col_temp:
        plantilla_json = json.dumps(st.session_state.mapeo_lista)
        st.download_button(
            "Guardar Configuración (JSON)",
            plantilla_json,
            "mi_plantilla.json",
            "application/json"
        )

    if 'df_final' in st.session_state:
        st.markdown("<div class='divider-fancy'></div>",
                    unsafe_allow_html=True)
        st.subheader("Descarga de Resultado")

        col_dl1, col_dl2, col_dl3 = st.columns(3)

        # EXCEL
        with col_dl1:
            output = BytesIO()
            st.session_state.df_final.to_excel(output, index=False)
            st.download_button(
                "Descargar EXCEL",
                output.getvalue(),
                "reporte_final.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        # CSV
        with col_dl2:
            csv = st.session_state.df_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Descargar CSV",
                csv,
                "reporte_final.csv",
                "text/csv",
                use_container_width=True
            )

        # JSON
        with col_dl3:
            json_str = st.session_state.df_final.to_json(
                orient='records', force_ascii=False)
            st.download_button(
                "Descargar JSON",
                json_str,
                "reporte_final.json",
                "application/json",
                use_container_width=True
            )
# FOOTER
st.markdown("<div class='divider-fancy'></div>", unsafe_allow_html=True)
