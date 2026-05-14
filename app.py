import streamlit as st
import easyocr
import cv2
import numpy as np
from PIL import Image

# Списък с потенциално вредни съставки (може да се разшири)
HARMFUL_INGREDIENTS = [
    "aspartame", "msg", "high fructose corn syrup", "palm oil", 
    "sodium nitrite", "bha", "bht", "artificial color", "trans fat",
    "аспартам", "палмово масло", "глутамат", "натриев нитрит"
]

def process_image(image):
    # Конвертиране на PIL изображение към numpy array за EasyOCR
    img_array = np.array(image)
    reader = easyocr.Reader(['en', 'bg']) # Поддръжка на английски и български
    result = reader.readtext(img_array, detail=0)
    return " ".join(result).lower()

# --- Потребителски интерфейс ---
st.set_page_config(page_title="Скенер за съставки", page_icon="🥗")
st.title("🔍 Скенер за вредни съставки")
st.write("Качете снимка на етикета със съдържанието, за да проверите за вредни добавки.")

# Опция за качване или снимане
source = st.radio("Изберете източник:", ("Качване на снимка", "Използване на камера"))

if source == "Качване на снимка":
    uploaded_file = st.file_uploader("Изберете файл...", type=["jpg", "jpeg", "png"])
else:
    uploaded_file = st.camera_input("Снимайте етикета")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Вашата снимка', use_container_width=True)
    
    with st.spinner('Анализиране на текста...'):
        extracted_text = process_image(image)
        
        # Логика за сортиране
        found_harmful = [ing for ing in HARMFUL_INGREDIENTS if ing in extracted_text]
        
    st.divider()
    
    # Резултати
    if found_harmful:
        st.error(f"⚠️ Внимание! Открити са следните вредни съставки:")
        for item in found_harmful:
            st.write(f"- **{item.capitalize()}**")
    else:
        st.success("✅ Не са открити познати вредни съставки в базата данни.")
    
    with st.expander("Виж извлечения текст от етикета"):
        st.write(extracted_text)
