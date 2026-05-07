import streamlit as st
import easyocr
from PIL import Image
import numpy as np

# Настройка на заглавието на страницата
st.set_page_config(page_title="EasyOCR Български & English", page_icon="📝")

st.title("📝 Текст от изображение (OCR)")
st.subheader("Поддържа български и английски език")

# Функция за кеширане на модела, за да не се зарежда при всяко кликване
@st.cache_resource
def load_model():
    # Зареждаме 'bg' за български и 'en' за английски
    return easyocr.Reader(['bg', 'en'], gpu=False) # Смени на gpu=True, ако имаш NVIDIA карта

reader = load_model()

# Компонент за качване на снимка
uploaded_file = st.file_uploader("Избери снимка...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Показване на каченото изображение
    image = Image.open(uploaded_file)
    st.image(image, caption='Качена снимка', use_container_width=True)
    
    st.write("---")
    
    with st.spinner('Обработка и разпознаване на текста...'):
        try:
            # Превръщане на Pillow изображението в numpy array за EasyOCR
            img_array = np.array(image)
            
            # Извличане на текста
            results = reader.readtext(img_array)
            
            if results:
                st.success("Текстът е извлечен успешно!")
                
                # Обединяване на всички намерени текстови блокове
                full_text = "\n".join([res[1] for res in results])
                
                # Показване на текста в текстово поле
                st.text_area("Резултат:", value=full_text, height=300)
                
                # Бутон за изтегляне на резултата
                st.download_button(
                    label="Изтегли текста като .txt",
                    data=full_text,
                    file_name="extracted_text.txt",
                    mime="text/plain"
                )
            else:
                st.warning("Не беше открит текст в изображението.")
                
        except Exception as e:
            st.error(f"Възникна грешка при обработката: {e}")

else:
    st.info("Моля, качете снимка, за да започнете.")
