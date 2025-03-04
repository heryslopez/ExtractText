import streamlit as st
import pytesseract
from PIL import Image, ImageEnhance
from langdetect import detect
from deep_translator import GoogleTranslator

# Configurar Tesseract
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Interfaz
st.title("Extraer y Traducir Texto de Imágenes")

# Inicializar session_state
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "detected_lang" not in st.session_state:
    st.session_state.detected_lang = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "apply_processing" not in st.session_state:
    st.session_state.apply_processing = False

# Función para preprocesar imagen
def preprocess_image(image):
    image = image.convert("L")
    enhancer = ImageEnhance.Contrast(image).enhance(2.0)
    image = ImageEnhance.Brightness(image).enhance(1.2)
    return image

# Subir imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen Original", width=300)
    
    # Checkbox para activar/desactivar el procesamiento
    st.session_state.apply_processing = st.checkbox("Aplicar procesamiento de imagen")
    
    processed_image = preprocess_image(image) if st.session_state.apply_processing else image
    st.image(processed_image, caption="Imagen Procesada" if st.session_state.apply_processing else "Imagen sin Procesar", width=300)

    if st.button("Extraer Texto"):
        with st.spinner("Extrayendo texto..."):
            try:
                text = pytesseract.image_to_string(processed_image)
                if text.strip():
                    st.session_state.extracted_text = text
                    st.session_state.detected_lang = detect(text)
                else:
                    st.warning("No se pudo extraer texto. Asegúrate de que la imagen sea clara.")
            except Exception as e:
                st.error(f"Error al procesar la imagen: {e}")

# Mostrar resultados si hay texto extraído
if st.session_state.extracted_text:
    st.write(f"Idioma detectado: {st.session_state.detected_lang}")
    st.text_area("Texto Extraído", st.session_state.extracted_text, height=200)
    
    # Selección de idioma para traducción
    target_lang = st.selectbox("Traducir a", GoogleTranslator().get_supported_languages())
    if st.button("Traducir Texto"):
        with st.spinner("Traduciendo..."):
            st.session_state.translated_text = GoogleTranslator(source=st.session_state.detected_lang, target=target_lang).translate(st.session_state.extracted_text)
    
    # Mostrar texto traducido si existe
    if st.session_state.translated_text:
        st.text_area("Texto Traducido", st.session_state.translated_text, height=200)
