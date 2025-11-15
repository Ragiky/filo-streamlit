import streamlit as st
from pathlib import Path
from typing import Set

st.set_page_config(page_title="Filo", layout="wide")

# Quitar bordes blancos, menú y padding del contenedor principal
st.markdown(
    """
    <style>
    header, footer, [data-testid="stToolbar"] {display: none !important;}
    .appview-container .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    .stApp {margin: 0 !important; padding: 0 !important;}
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
        # Botón para cerrar sesión manualmente
        c1, _ = st.columns([1, 20])
        with c1:
            if st.button("Cerrar sesión"):
                st.session_state["authed"] = False
                st.query_params["token"] = ""
                st.rerun()

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