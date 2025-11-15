import streamlit as st
from pathlib import Path
from typing import Set

st.set_page_config(page_title="Filo", layout="wide")

# Quitar bordes blancos, menú y padding del contenedor principal
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=IM+Fell+English+SC&display=swap');
    header, footer, [data-testid="stToolbar"] {display: none !important;}
    .appview-container .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    .stApp {margin: 0 !important; padding: 0 !important;}
    .logout-btn {
        position: fixed;
        top: 18px;
        right: 18px;
        background: radial-gradient(circle at 30% 20%, #f8f2e4 0%, #efe6d1 60%, #e7dcc4 100%);
        color: #2b1b0f !important;
        padding: 10px 16px 10px 40px;
        border-radius: 12px;
        border: 2px solid #7a4f2b;
        box-shadow: 0 10px 24px rgba(122,79,43,0.25), inset 0 2px 0 rgba(255,255,255,0.6);
        font-weight: 700;
        font-family: 'Cinzel', 'IM Fell English SC', serif;
        letter-spacing: 0.4px;
        text-decoration: none !important;
        z-index: 9999;
        transition: transform 0.08s ease, box-shadow 0.18s ease;
        text-shadow: 0 1px 0 rgba(255,255,255,0.6);
    }
    .logout-btn::before {
        content: '⚔';
        position: absolute;
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
        width: 22px;
        height: 22px;
        line-height: 22px;
        text-align: center;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #b6172f 0%, #7f0d1e 60%, #5c0a17 100%);
        color: #f6d6d6;
        box-shadow: 0 4px 10px rgba(92,10,23,0.35), inset 0 1px 0 rgba(255,255,255,0.4);
        font-family: 'Cinzel', serif;
        font-size: 14px;
    }
    .logout-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 28px rgba(122,79,43,0.32), inset 0 2px 0 rgba(255,255,255,0.7);
    }
    .logout-btn:active {
        transform: translateY(0);
        box-shadow: 0 8px 18px rgba(122,79,43,0.28), inset 0 1px 0 rgba(255,255,255,0.5);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

html_path = Path(__file__).parent / "Filo.html"
if not html_path.exists():
    st.error("No se encontró Filo.html en el directorio actual.")
    st.write(f"Ruta esperada: {html_path}")
else:
    # Puerta de acceso por token (vía query string o input)
    ALLOWED_TOKENS: Set[str] = {"demo123", "elchesquito"}  # Cambia/añade tokens aquí
    # Leer token de la URL de forma robusta (normaliza claves y tipos)
    def _get_token_from_query() -> str:
        try:
            qp_items = dict(st.query_params.items())
        except Exception:
            qp_items = {}
        # normalizar claves a minúsculas
        normalized = {str(k).lower(): v for k, v in qp_items.items()}
        raw = normalized.get("token")
        if isinstance(raw, list):
            val = raw[0] if raw else ""
        elif isinstance(raw, str):
            val = raw
        else:
            val = ""
        return val.strip()

    token = _get_token_from_query()

    # Inicializar estado de sesión
    if "authed" not in st.session_state:
        st.session_state["authed"] = False
    # Si el token en la URL es válido, marcar sesión como autenticada
    if token in ALLOWED_TOKENS:
        st.session_state["authed"] = True

    # Soporte de cierre de sesión vía parámetro de consulta (?logout=1)
    def _get_logout_flag() -> bool:
        raw = st.query_params.get("logout")
        if isinstance(raw, list):
            s = raw[0] if raw else ""
        elif isinstance(raw, str):
            s = raw
        else:
            s = ""
        return str(s).strip().lower() in {"1", "true", "yes"}

    if _get_logout_flag():
        st.session_state["authed"] = False
        # limpiar token de la URL para evitar re-autenticación automática
        st.query_params["token"] = ""
        st.query_params["logout"] = ""
        st.rerun()
    # Mostrar formulario solo si no está autenticado
    if not st.session_state.get("authed", False):
        st.markdown("## Acceso restringido")
        st.write("Ingresa el token de acceso para ver el contenido.")
        input_token = st.text_input("Token", type="password")
        submit = st.button("Entrar")
        if submit:
            if input_token in ALLOWED_TOKENS:
                st.session_state["authed"] = True
                st.query_params["token"] = input_token
                st.rerun()
            else:
                st.error("Token inválido. Revisa el que te compartieron.")

    if st.session_state.get("authed", False):
        # Botón flotante dentro de la página (estilo DnD)
        st.markdown('<a class="logout-btn" href="?logout=1">Cerrar sesión</a>', unsafe_allow_html=True)

        html_content = html_path.read_text(encoding="utf-8")
        # Asegurar que el contenido ocupe toda la altura visible y sin márgenes
        if "</head>" in html_content:
            html_content = html_content.replace(
                "</head>",
                "<style>html,body{margin:0;padding:0;height:100vh;}</style></head>",
            )
        else:
            html_content = (
                "<style>html,body{margin:0;padding:0;height:100vh;}</style>" + html_content
            )
        st.components.v1.html(html_content, height=1000, scrolling=True)