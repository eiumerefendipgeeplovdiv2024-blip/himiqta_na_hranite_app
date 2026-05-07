import streamlit as st
import easyocr
from PIL import Image
import numpy as np

st.set_page_config(page_title="Health Scanner OCR", page_icon="🥗")

# 1. Дефиниране на списъци със съставки
# Можеш да ги разшириш по твой избор
BAD_INGREDIENTS = [
    "захар", "sugar", "палмово масло", "palm oil", "e621", "msg", 
    "аспартам", "aspartame", "консервант", "preservative", "оцветител"
]
GOOD_INGREDIENTS = [
    "витамин", "vitamin", "протеин", "protein", "фибри", "fiber", 
    "омега", "omega", "магнезий", "magnesium", "натурално", "natural"
]

@st.cache_resource
def load_model():
    return easyocr.Reader(['bg', 'en'], gpu=False)

reader = load_model()

st.title("🥗 Анализатор на съставки")
st.write("Качете снимка на етикет, за да проверим съдържанието.")

uploaded_file = st.file_uploader("Избери снимка...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Етикет за анализ', use_container_width=True)
    
    with st.spinner('Анализиране...'):
        img_array = np.array(image)
        results = reader.readtext(img_array)
        
        if results:
            # Обединяваме целия текст и го правим с малки букви за по-лесно търсене
            full_text = " ".join([res[1].lower() for res in results])
            
            # Логика за сортиране
            found_bad = [item for item in BAD_INGREDIENTS if item in full_text]
            found_good = [item for item in GOOD_INGREDIENTS if item in full_text]

            # Визуализация с колони
            st.subheader("📊 Резултати от анализа")
            col1, col2 = st.columns(2)

            with col1:
                st.error("⚠️ Вредни / Спорни")
                if found_bad:
                    for item in found_bad:
                        st.write(f"❌ {item.capitalize()}")
                else:
                    st.write("Не са открити критични съставки.")

            with col2:
                st.success("✅ Полезни / Позитивни")
                if found_good:
                    for item in found_good:
                        st.write(f"⭐ {item.capitalize()}")
                else:
                    st.write("Няма открити специфични полезни съставки.")

            st.write("---")
            with st.expander("Виж целия разпознат текст"):
                st.text(full_text)
        else:
            st.warning("Не можах да разчета текст. Опитайте с по-чиста снимка.")
