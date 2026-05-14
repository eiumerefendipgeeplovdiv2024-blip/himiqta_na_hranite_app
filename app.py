import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import json

# Настройка на страницата
st.set_page_config(page_title="Анализатор на съставки", page_icon="🔍")

st.title("🔍 Скенер за вредни съставки")
st.write("Качете снимка на етикета със съставките (от опаковката), за да направим анализ.")

# Поле за API ключ
api_key = st.text_input("Въведете вашия Google Gemini API ключ:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # СЕКЦИЯ ЗА КАЧВАНЕ НА СНИМКА
    uploaded_file = st.file_uploader("Изберете снимка от вашето устройство...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Показване на качената снимка
        image = Image.open(uploaded_file)
        st.image(image, caption='Качена снимка', width=300)
        
        if st.button("🚀 Анализирай съставките"):
            with st.spinner("AI анализира съдържанието..."):
                try:
                    prompt = """
                    Анализирай тази снимка на етикет:
                    1. Извади списък със съставките.
                    2. Раздели ги в таблица със следните колони: 
                       - 'Съставка'
                       - 'Статус' (Вредна или Невредна)
                       - 'Бъдещи ефекти' (какви са негативните последствия при редовна консумация).
                    3. Върни резултата под формата на JSON.
                    """
                    
                    response = model.generate_content([prompt, image])
                    
                    # Изчистване на текста от AI за JSON
                    raw_text = response.text.replace('```json', '').replace('```', '').strip()
                    data = json.loads(raw_text)
                    
                    # Създаване на таблицата
                    df = pd.DataFrame(data)
                    
                    # Визуализация
                    st.subheader("📊 Резултати от анализа")
                    st.table(df) # Използваме st.table за по-прегледно изписване на дългите текстове

                    st.warning("⚠️ Забележка: Резултатите са генерирани от AI и са с информативна цел. Винаги се консултирайте със специалист при здравословни проблеми.")

                except Exception as e:
                    st.error(f"Грешка: Не можах да разчета текста добре. Моля, опитайте с по-чиста снимка. Детайли: {e}")

else:
    st.info("Моля, поставете своя API ключ в полето по-горе, за да активирате скенера.")
