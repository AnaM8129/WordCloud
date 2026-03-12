"""
☁️ WordCloud Studio — Nube de Palabras Profesional
Rediseño: editorial de lujo, dark mode orgánico

Instalación:
    pip install streamlit wordcloud matplotlib pandas Pillow numpy

Ejecución:
    streamlit run wordcloud_app.py
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import io
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="WordCloud Studio",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Variables ── */
:root {
    --ink:       #0c0a08;
    --paper:     #13110e;
    --surface:   #1c1916;
    --lift:      #252118;
    --border:    rgba(255,220,120,0.10);
    --border2:   rgba(255,220,120,0.20);
    --gold:      #e8c97a;
    --gold-soft: #c4a55a;
    --cream:     #f0e6cc;
    --muted:     #8a7f6a;
    --dim:       #5a5040;
    --accent:    #d4845a;
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
    background: var(--paper) !important;
    font-family: 'Syne', sans-serif;
    color: var(--cream);
}

/* ── Noise overlay ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.6;
}

/* ── Hide chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1280px !important;
    margin: 0 auto !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--ink) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--gold-soft); border-radius: 2px; opacity: 0.4; }

/* ── Typography ── */
h1 {
    font-family: 'Playfair Display', serif !important;
    color: var(--cream) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}
h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--cream) !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    font-size: 0.7rem !important;
    color: var(--gold) !important;
}
p { color: var(--muted) !important; font-size: 0.9rem !important; line-height: 1.75 !important; }
label { color: var(--muted) !important; font-size: 0.8rem !important; font-family: 'Syne', sans-serif !important; }

/* ── Sidebar labels ── */
section[data-testid="stSidebar"] label {
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}
section[data-testid="stSidebar"] p { color: var(--dim) !important; font-size: 0.82rem !important; }

/* ── Inputs & textareas ── */
textarea, input[type="text"], .stTextInput input, .stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--cream) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    caret-color: var(--gold) !important;
}
textarea:focus, input:focus {
    border-color: var(--gold-soft) !important;
    box-shadow: 0 0 0 2px rgba(232,201,122,0.08) !important;
    outline: none !important;
}

/* ── Select ── */
[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--cream) !important;
    font-size: 0.85rem !important;
}
[data-baseweb="select"] * { color: var(--cream) !important; }
[data-baseweb="menu"] { background: var(--lift) !important; border: 1px solid var(--border2) !important; }
[data-baseweb="option"]:hover { background: var(--surface) !important; }

/* ── Slider ── */
[data-testid="stSlider"] > div > div { background: var(--surface) !important; }
[data-testid="stSlider"] [data-testid="stThumbValue"] { color: var(--gold) !important; }

/* ── Radio ── */
[data-testid="stRadio"] label { color: var(--muted) !important; }
[data-testid="stRadio"] [data-baseweb="radio"] div:first-child {
    border-color: var(--border2) !important;
    background: transparent !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border2) !important;
    border-radius: 3px !important;
    color: var(--gold) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    background: rgba(232,201,122,0.07) !important;
    border-color: var(--gold) !important;
    color: var(--cream) !important;
    box-shadow: 0 0 20px rgba(232,201,122,0.08) !important;
}

/* Primary generate button */
section[data-testid="stSidebar"] .stButton:last-of-type > button {
    background: var(--gold) !important;
    border-color: var(--gold) !important;
    color: var(--ink) !important;
    font-weight: 800 !important;
    letter-spacing: 0.15em !important;
}
section[data-testid="stSidebar"] .stButton:last-of-type > button:hover {
    background: var(--cream) !important;
    border-color: var(--cream) !important;
    box-shadow: 0 4px 24px rgba(232,201,122,0.25) !important;
}

/* Download button */
[data-testid="stDownloadButton"] button {
    background: transparent !important;
    border: 1px solid var(--border2) !important;
    color: var(--gold-soft) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-radius: 3px !important;
}
[data-testid="stDownloadButton"] button:hover {
    border-color: var(--gold) !important;
    color: var(--gold) !important;
    background: rgba(232,201,122,0.05) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: 2px solid var(--gold-soft) !important;
    border-radius: 4px !important;
    padding: 20px 24px !important;
}
[data-testid="metric-container"] label {
    color: var(--dim) !important;
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-family: 'Syne', sans-serif !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--cream) !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}
div[data-testid="stExpander"] summary { color: var(--muted) !important; font-size: 0.82rem !important; }

/* ── Alerts ── */
.stSuccess { background: rgba(100,180,100,0.08) !important; border-left: 3px solid #64b464 !important; border-radius: 4px !important; }
.stWarning { background: rgba(232,201,122,0.08) !important; border-left: 3px solid var(--gold-soft) !important; border-radius: 4px !important; }
.stError   { background: rgba(212,132,90,0.08)  !important; border-left: 3px solid var(--accent) !important; border-radius: 4px !important; }

/* ── Dataframe ── */
.stDataFrame { border-radius: 4px !important; overflow: hidden !important; border: 1px solid var(--border) !important; }
[data-testid="stDataFrameResizable"] { background: var(--surface) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 20px 0 !important; }

/* ── Custom elements ── */
.studio-hero {
    padding: 48px 0 40px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 36px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 24px;
}
.studio-hero .eyebrow {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold-soft);
    margin-bottom: 10px;
    font-family: 'Syne', sans-serif;
}
.studio-hero h1 {
    font-size: 3.2rem !important;
    line-height: 1.05 !important;
    margin: 0 !important;
    color: var(--cream) !important;
}
.studio-hero h1 em {
    font-style: italic;
    color: var(--gold) !important;
}
.studio-hero .desc {
    color: var(--dim);
    font-size: 0.85rem;
    margin-top: 12px;
    max-width: 480px;
    line-height: 1.7;
    font-family: 'Syne', sans-serif;
}

.sidebar-brand {
    padding: 28px 20px 20px;
    border-bottom: 1px solid var(--border);
}
.sidebar-brand .name {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    color: var(--cream);
    font-style: italic;
}
.sidebar-brand .tagline {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--dim);
    margin-top: 3px;
    font-family: 'Syne', sans-serif;
}

.sidebar-section {
    padding: 20px;
    border-bottom: 1px solid var(--border);
}
.section-label {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold-soft);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Syne', sans-serif;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

.info-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 18px 20px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.info-card:hover { border-color: var(--border2); }
.info-card .ic-icon { font-size: 1.1rem; margin-bottom: 8px; }
.info-card .ic-title {
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--cream);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-family: 'Syne', sans-serif;
}
.info-card .ic-desc { font-size: 0.82rem; color: var(--muted); margin-top: 3px; line-height: 1.55; }

.freq-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 9px 14px;
    margin: 3px 0;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 3px;
    transition: border-color 0.15s, background 0.15s;
}
.freq-row:hover { border-color: var(--border2); background: var(--lift); }

.rank-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--dim);
    min-width: 28px;
    font-weight: 500;
}
.freq-word {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--cream);
    min-width: 120px;
    font-family: 'Syne', sans-serif;
}
.freq-bar {
    height: 3px;
    background: linear-gradient(90deg, var(--gold-soft), var(--gold));
    border-radius: 2px;
    display: inline-block;
}
.freq-count {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--gold-soft);
    min-width: 24px;
    text-align: right;
    margin-left: auto;
}

.wc-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 12px;
}
.wc-topbar {
    padding: 12px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}
.wc-topbar .wc-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--gold-soft);
}
.wc-topbar .wc-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--dim);
}
.wc-body { padding: 0; }

.tag-pill {
    display: inline-block;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--muted);
    margin: 3px 2px;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.03em;
    transition: border-color 0.15s;
}
.tag-pill:hover { border-color: var(--border2); color: var(--cream); }

.palette-swatch {
    display: flex;
    gap: 4px;
    align-items: center;
    margin: 4px 0;
}
.palette-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}
.palette-name {
    font-size: 0.78rem;
    color: var(--muted);
    margin-left: 6px;
    font-family: 'Syne', sans-serif;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STOPWORDS
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
    "habian","tiene","tienen","hacer","puede","pueden","asi","tan","parte","todo","todos",
    "todas","cada","otro","otra","otros","otras","mismo","misma","nuestro","nuestra",
    "ellos","ellas","nosotros","les","esa","esos","esas","aquel","aquella","aquellos",
}

def obtener_stopwords(idioma):
    sw = set(STOPWORDS)
    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES
    return sw


# ─────────────────────────────────────────────
# PALETAS
# ─────────────────────────────────────────────
PALETAS = {
    "Ámbar nocturno":       ["#e8c97a","#c4a55a","#a07830","#d4845a","#f0e6cc","#8a6a30","#604820"],
    "Escala de grises":     ["#f0ece4","#c8c0b0","#988880","#685850","#403830","#282018","#181008"],
    "Azul marino":          ["#93c5fd","#60a5fa","#3b82f6","#2563eb","#1d4ed8","#1e3a5f","#0f2942"],
    "Verde salvia":         ["#6ee7b7","#34d399","#10b981","#059669","#047857","#065f46","#064e3b"],
    "Terracota":            ["#fdba74","#fb923c","#f97316","#ea580c","#c2410c","#9a3412","#7c2d12"],
    "Índigo profundo":      ["#a5b4fc","#818cf8","#6366f1","#4f46e5","#4338ca","#3730a3","#312e81"],
    "Monocromático negro":  ["#ffffff","#cccccc","#aaaaaa","#888888","#666666","#444444","#222222"],
}

FORMAS = {
    "Rectángulo": None,
    "Círculo":    "circle",
}

def crear_mascara(forma, size=500):
    if forma == "circle":
        y, x = np.ogrid[:size, :size]
        cx, cy = size // 2, size // 2
        mascara = np.ones((size, size), dtype=np.uint8) * 255
        mascara[(x - cx)**2 + (y - cy)**2 <= (size // 2 - 12)**2] = 0
        return mascara
    return None


# ─────────────────────────────────────────────
# FUNCIONES CORE
# ─────────────────────────────────────────────
def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñàâèêîôùûäëïöü\s]", " ", texto, flags=re.UNICODE)
    palabras = [p for p in texto.split() if p not in stopwords and len(p) >= min_longitud]
    return " ".join(palabras)

def contar_palabras(texto_limpio):
    return pd.DataFrame(Counter(texto_limpio.split()).most_common(50),
                        columns=["Palabra", "Frecuencia"])

def generar_wordcloud(texto_limpio, paleta_nombre, max_words, fondo, forma, ancho=1000, alto=500):
    import random
    colores = PALETAS[paleta_nombre]
    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        rng = random_state or random.Random()
        return colores[rng.randint(0, len(colores) - 1)]
    mascara = crear_mascara(forma, size=min(ancho, alto))
    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words,
        background_color=fondo, color_func=color_func,
        mask=mascara, collocations=False,
        min_font_size=11, max_font_size=120,
        prefer_horizontal=0.75, relative_scaling=0.5, margin=5,
    ).generate(texto_limpio)
    fig, ax = plt.subplots(figsize=(ancho / 100, alto / 100))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(fondo)
    plt.tight_layout(pad=0)
    return fig

def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="name">WordCloud Studio</div>
        <div class="tagline">Análisis léxico visual</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Fuente ──
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Fuente de texto</div>', unsafe_allow_html=True)
    fuente = st.radio("fuente", ["✍️ Escribir / Pegar", "📂 Subir archivo"],
                      label_visibility="collapsed")
    texto_input = ""

    if fuente == "✍️ Escribir / Pegar":
        texto_input = st.text_area(
            "Texto:", height=175,
            placeholder="Pega aquí un artículo, reseña, discurso...",
            label_visibility="collapsed")

        with st.expander("Cargar texto de ejemplo"):
            ejemplos = {
                "Inteligencia Artificial": """
                La inteligencia artificial es una disciplina de la informática orientada a desarrollar
                sistemas capaces de ejecutar tareas que requieren capacidades cognitivas humanas.
                El aprendizaje automático, las redes neuronales profundas y el procesamiento del
                lenguaje natural constituyen los pilares técnicos de los sistemas modernos de
                inteligencia artificial. Los modelos de lenguaje de gran escala, la visión
                computacional y la robótica autónoma representan aplicaciones de vanguardia.
                """,
                "Colombia": """
                Colombia es una nación situada en el extremo noroccidental de América del Sur,
                reconocida por su excepcional biodiversidad, riqueza cultural y diversidad de paisajes.
                Bogotá es la capital y principal centro económico, seguida de Medellín, Cali y
                Barranquilla como ciudades de relevancia nacional. El café colombiano goza de
                reconocimiento internacional por su calidad y perfil aromático.
                """,
                "Tecnología 4.0": """
                La cuarta revolución industrial redefine los modelos productivos mediante la
                convergencia de tecnologías digitales avanzadas. El Internet de las cosas,
                la inteligencia artificial, el análisis de grandes datos, la robótica colaborativa
                y la automatización inteligente son pilares estratégicos de la industria moderna.
                """,
            }
            ejemplo_sel = st.selectbox("Ejemplo:", list(ejemplos.keys()),
                                       label_visibility="collapsed")
            if st.button("Cargar ejemplo"):
                st.session_state["texto_ejemplo"] = ejemplos[ejemplo_sel]
                st.rerun()

        if "texto_ejemplo" in st.session_state and not texto_input:
            texto_input = st.session_state["texto_ejemplo"]
    else:
        archivo = st.file_uploader("Archivo:", type=["txt", "csv"],
                                   label_visibility="collapsed")
        if archivo:
            if archivo.name.endswith(".txt"):
                texto_input = archivo.read().decode("utf-8", errors="ignore")
            elif archivo.name.endswith(".csv"):
                df_csv = pd.read_csv(archivo)
                col_txt = st.selectbox("Columna de texto:", df_csv.columns.tolist())
                texto_input = " ".join(df_csv[col_txt].dropna().astype(str).tolist())
            st.success(f"✓ Cargado — {len(texto_input):,} caracteres")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Procesamiento ──
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Procesamiento</div>', unsafe_allow_html=True)
    idioma         = st.selectbox("Stopwords:", ["Español", "Inglés", "Ambos", "Ninguno"])
    min_longitud   = st.slider("Longitud mínima", 2, 8, 3)
    palabras_extra = st.text_input("Excluir palabras:",
                                   placeholder="también, así, aquí",
                                   label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Apariencia ──
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Apariencia</div>', unsafe_allow_html=True)
    paleta_sel  = st.selectbox("Paleta de color:", list(PALETAS.keys()))

    # swatches visuales
    dots = "".join([f'<span class="palette-dot" style="background:{c};"></span>' for c in PALETAS[paleta_sel][:6]])
    st.markdown(f'<div class="palette-swatch">{dots}</div>', unsafe_allow_html=True)

    fondo_sel   = st.radio("Fondo:", ["Negro", "Blanco"], horizontal=True)
    fondo_color = "black" if fondo_sel == "Negro" else "white"
    forma_sel   = st.selectbox("Forma:", list(FORMAS.keys()))
    max_words   = st.slider("Máximo de palabras:", 20, 200, 80)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="padding:20px;">', unsafe_allow_html=True)
    generar = st.button("↗ Generar nube", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="studio-hero">
    <div>
        <div class="eyebrow">Herramienta de análisis léxico</div>
        <h1>Word<em>Cloud</em><br>Studio</h1>
        <div class="desc">
            Frecuencia de términos. Visualización de corpus.<br>
            Stopwords inteligentes en español e inglés.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PANTALLA DE BIENVENIDA
# ─────────────────────────────────────────────
if not generar or not texto_input.strip():
    col_izq, col_der = st.columns([3, 2], gap="large")

    with col_izq:
        st.markdown("### Cómo funciona")
        for icono, titulo, desc in [
            ("◈", "Análisis de frecuencia", "Identifica los términos dominantes de cualquier corpus textual."),
            ("◉", "Filtrado inteligente", "Elimina automáticamente palabras vacías en español e inglés."),
            ("◐", "Paletas profesionales", "Selecciona entre 7 combinaciones cromáticas cuidadosamente diseñadas."),
            ("⬡", "Exportación HD", "Descarga la imagen en alta resolución y la tabla de frecuencias en CSV."),
        ]:
            st.markdown(
                f'<div class="info-card">'
                f'<div class="ic-icon">{icono}</div>'
                f'<div class="ic-title">{titulo}</div>'
                f'<div class="ic-desc">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("### Pasos")
        for n, paso in enumerate([
            "Ingresa o sube tu texto en el panel lateral.",
            "Configura idioma, paleta de color y forma.",
            "Pulsa **↗ Generar nube**.",
            "Descarga la imagen PNG o la tabla CSV.",
        ], 1):
            st.markdown(
                f'<div style="padding:10px 0; border-bottom:1px solid var(--border); '
                f'display:flex; gap:16px; align-items:baseline;">'
                f'<span style="font-family:\'JetBrains Mono\',monospace; font-size:0.7rem; '
                f'color:var(--gold-soft); font-weight:500; min-width:18px;">{n:02d}</span>'
                f'<span style="font-size:0.88rem; color:var(--muted);">{paso}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with col_der:
        st.markdown("### Aplicaciones")
        casos = [
            "📰 Análisis de prensa", "📋 Encuestas abiertas",
            "💬 Reseñas de clientes", "🎓 Textos académicos",
            "🗳️ Discursos políticos", "📚 Estudios literarios",
            "📊 Inteligencia de negocio", "🌐 Monitoreo de redes",
        ]
        pills = "".join([f'<span class="tag-pill">{c}</span>' for c in casos])
        st.markdown(f'<div style="margin-bottom:24px;">{pills}</div>', unsafe_allow_html=True)

        st.markdown("### Paletas disponibles")
        for nombre, colores in PALETAS.items():
            dots = "".join([f'<span class="palette-dot" style="background:{c};"></span>' for c in colores])
            st.markdown(
                f'<div style="display:flex; align-items:center; gap:8px; padding:8px 0; '
                f'border-bottom:1px solid var(--border);">'
                f'<div style="display:flex; gap:3px;">{dots}</div>'
                f'<span class="palette-name">{nombre}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if not texto_input.strip() and generar:
        st.warning("Ingresa un texto en el panel lateral antes de generar la nube.")
    st.stop()


# ─────────────────────────────────────────────
# PROCESAMIENTO
# ─────────────────────────────────────────────
stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
if palabras_extra.strip():
    stopwords_set |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

texto_limpio = limpiar_texto(texto_input, stopwords_set, min_longitud)

if not texto_limpio.strip():
    st.error("El texto resultante está vacío. Reduce la longitud mínima o cambia la configuración de stopwords.")
    st.stop()

df_freq        = contar_palabras(texto_limpio)
total_palabras = len(texto_limpio.split())
vocabulario    = len(df_freq)

# ── Métricas ──
m1, m2, m3, m4 = st.columns(4)
m1.metric("Palabras procesadas",   f"{total_palabras:,}")
m2.metric("Vocabulario único",     f"{vocabulario:,}")
m3.metric("Término principal",     df_freq.iloc[0]["Palabra"] if not df_freq.empty else "—")
m4.metric("Frecuencia máxima",     int(df_freq.iloc[0]["Frecuencia"]) if not df_freq.empty else 0)

st.markdown("<br>", unsafe_allow_html=True)

# ── Nube ──
with st.spinner("Generando..."):
    fig_wc = generar_wordcloud(
        texto_limpio, paleta_sel, max_words, fondo_color,
        FORMAS[forma_sel], ancho=1000, alto=500,
    )

st.markdown(
    f'<div class="wc-container">'
    f'<div class="wc-topbar">'
    f'<span class="wc-title">Nube de palabras</span>'
    f'<span class="wc-meta">{paleta_sel} · fondo {fondo_sel.lower()} · {max_words} palabras máx.</span>'
    f'</div>'
    f'<div class="wc-body">',
    unsafe_allow_html=True,
)
st.pyplot(fig_wc, use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

img_bytes = fig_a_bytes(fig_wc)
col_dl1, col_dl2, _ = st.columns([1, 1, 3])
with col_dl1:
    st.download_button(
        "⬇ Descargar PNG",
        data=img_bytes, file_name="wordcloud.png", mime="image/png",
        use_container_width=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div style="height:1px; background:var(--border); margin:8px 0 28px;"></div>',
            unsafe_allow_html=True)

# ── Análisis ──
col_freq, col_tabla = st.columns([3, 2], gap="large")

with col_freq:
    st.markdown("### Frecuencia léxica — Top 20")
    top20    = df_freq.head(20)
    max_freq = top20["Frecuencia"].max()

    for rank, (_, row) in enumerate(top20.iterrows(), 1):
        p = row["Palabra"]
        f = int(row["Frecuencia"])
        barra_w = max(10, int((f / max_freq) * 180))
        opacity = 0.45 + 0.55 * (f / max_freq)
        st.markdown(
            f'<div class="freq-row">'
            f'<span class="rank-tag">{rank:02d}</span>'
            f'<span class="freq-word">{p}</span>'
            f'<div class="freq-bar" style="width:{barra_w}px; opacity:{opacity:.2f};"></div>'
            f'<span class="freq-count">{f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with col_tabla:
    st.markdown("### Tabla de frecuencias")
    st.dataframe(
        df_freq.head(30).style
               .background_gradient(subset=["Frecuencia"], cmap="YlOrBr")
               .format({"Frecuencia": "{:,}"}),
        use_container_width=True, height=500,
    )
    csv_bytes = df_freq.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Exportar CSV",
        data=csv_bytes, file_name="frecuencias.csv", mime="text/csv",
        use_container_width=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("Ver texto procesado"):
    preview = texto_limpio[:2500] + ("..." if len(texto_limpio) > 2500 else "")
    st.markdown(
        f'<p style="font-family:\'JetBrains Mono\',monospace; font-size:0.8rem; '
        f'color:var(--muted); background:var(--surface); padding:18px 20px; '
        f'border-radius:4px; line-height:1.85;">{preview}</p>',
        unsafe_allow_html=True,
    )

plt.close("all")
