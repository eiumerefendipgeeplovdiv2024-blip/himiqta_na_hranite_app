import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# Списък с примерни "вредни" съставки (може да бъде разширен)
DANGEROUS_INGREDIENTS = [
    "E621", "monosodium glutamate", "мононатриев глутамат",
    "palm oil", "палмово масло", "палмова мазнина",
    "high fructose corn syrup", "глюкозо-фруктозен сироп",
    "aspartame", "аспартам", "E951",
    "hydrogenated fat", "хидрогенирани мазнини"
]

def process_image(image):
    # Инициализиране на OCR (зарежда модела при първо извикване)
    reader = easyocr.Reader(['bg', 'en'])
    
    # Конвертиране на PIL изображението в numpy array за EasyOCR
    img_array = np.array(image)
    
    with st.spinner('Анализиране на текста...'):
        results = reader.readtext(img_array, detail=0)
    return results

def check_for_ingredients(text_list):
    found = []
    # Обединяваме целия текст в един низ за по-лесно търсене
    full_text = " ".join(text_list).lower()
    
    for ingredient in DANGEROUS_INGREDIENTS:
        if ingredient.lower() in full_text:
            found.append(ingredient)
    return found

# --- STREAMLIT UI ---
st.set_page_config(page_title="Скенер за съставки", page_icon="🔍")
st.title("🔍 Скенер за вредни съставки")
st.write("Качете снимка на етикета или използвайте камерата си.")

# Опции за източник на изображението
source_option = st.radio("Изберете източник:", ("Качване на файл", "Камера"))

uploaded_file = None
if source_option == "Качване на файл":
    uploaded_file = st.file_uploader("Изберете снимка...", type=["jpg", "jpeg", "png"])
else:
    uploaded_file = st.camera_input("Направете снимка на етикета")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Вашата снимка', use_column_width=True)
    
    if st.button('Анализирай състава'):
        extracted_text = process_image(image)
        
        if extracted_text:
            st.subheader("Разпознат текст:")
            st.info(" ".join(extracted_text))
            
            # Проверка за съставки
            found_bad_stuff = check_for_ingredients(extracted_text)
            
            st.divider()
            
            if found_bad_stuff:
                st.error(f"⚠️ Внимание! Открити са следните съставки: {', '.join(found_bad_stuff)}")
            else:
                st.success("✅ Не бяха открити съставки от списъка с вредни вещества.")
        else:
            st.warning("Не беше открит текст на снимката. Опитайте с по-добро осветление.")
