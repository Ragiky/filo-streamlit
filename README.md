# Filo (Streamlit)

Este proyecto muestra `Filo.html` dentro de una app de Streamlit con control de acceso por token vía query string (`?token=...`).

## Ejecutar localmente

1. Instala dependencias:
   - `pip install -r requirements.txt`
2. Inicia la app:
   - `python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501`
3. Abre:
   - Local: `http://127.0.0.1:8501/?token=demo123`

## Despliegue en Streamlit Cloud (URL estable en `streamlit.app`)

Streamlit Cloud ofrece una URL persistente tipo `https://<tu-app>.streamlit.app`. No soporta dominio personalizado (`filo.takeshi.com`) en el plan estándar.

Pasos:
1. Sube esta carpeta a un repositorio en GitHub.
2. Ve a https://streamlit.io/cloud y despliega el repo.
3. Elige un nombre de app (por ejemplo `filo-takeshi`).
4. Accede: `https://filo-takeshi.streamlit.app/?token=demo123`.

## Dominio personalizado `filo.takeshi.com` (opción con Cloudflare Tunnel)

Si necesitas `filo.takeshi.com`, usa Cloudflare Tunnel con un dominio que administres en Cloudflare.

1. `cloudflared login` y selecciona `takeshi.com`.
2. `cloudflared tunnel create filo-app` y copia el `Tunnel UUID`.
3. Edita `cloudflared_config.yml` con:
   - `tunnel: <TUNNEL_UUID>`.
   - `credentials-file: C:\\Users\\<usuario>\\.cloudflared\\<TUNNEL_UUID>.json`.
   - `hostname: filo.takeshi.com` apuntando a `http://localhost:8501`.
4. DNS: `cloudflared tunnel route dns filo-app filo.takeshi.com`.
5. Ejecuta: `cloudflared tunnel --config cloudflared_config.yml run filo-app`.
6. Accede: `https://filo.takeshi.com/?token=demo123`.

Notas:
- Cambia/añade tokens permitidos en `ALLOWED_TOKENS` dentro de `app.py`.
- Para cerrar sesión: `?logout=1` o el botón "Cerrar sesión".