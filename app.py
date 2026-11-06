import os
import streamlit as st
import yt_dlp

st.set_page_config(page_title="Mi Descargador Personal de YouTube", page_icon="🎵", layout="centered")

st.markdown("<h1 style='text-align: center;'>🎵 Mi Descargador Personal de YouTube</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Pega tu enlace, selecciona el formato de máxima calidad y descarga directamente con metadatos y carátula.</p>", unsafe_allow_html=True)

enlace = st.text_input("Pega tu enlace de YouTube aquí:")

formato_opciones = {
    "MP3 (320 kbps estándar)": "mp3",
    "FLAC (Máxima calidad sin pérdida)": "flac",
    "WAV (Audio sin comprimir)": "wav",
    "M4A (Alta calidad AAC)": "m4a"
}

formato_seleccionado = st.selectbox("Selecciona el formato de audio:", list(formato_opciones.keys()))
formato_extension = formato_opciones[formato_seleccionado]

if st.button("Convertir y Descargar"):
    if not enlace:
        st.warning("Por favor, introduce un enlace válido de YouTube.")
    else:
        output_dir = "Musica"
        os.makedirs(output_dir, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': formato_extension,
                    'preferredquality': '320',
                },
                {
                    'key': 'EmbedThumbnail',  # Incrusta la miniatura como carátula del archivo
                },
                {
                    'key': 'FFmpegMetadata',   # Añade título, artista y datos de la canción
                },
            ],
            'writethumbnail': True,  # Necesario para extraer la miniatura de YouTube
        }

        try:
            with st.spinner("Descargando y procesando audio, metadatos y carátula... Espera un momento."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([enlace])
            st.success(f"¡Listo! Tu canción se ha descargado y guardado en la carpeta **Musica** con sus metadatos.")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")