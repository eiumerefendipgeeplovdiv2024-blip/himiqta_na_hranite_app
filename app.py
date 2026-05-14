import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import json

# Настройка на страницата
st.set_page_config(page_title="Скенер за съставки", page_icon="🍏", layout="wide")

st.title("Скенер за съставки 🕵️‍♀️🍏")
st.write("Качете снимка на етикета със съставките или го снимайте с камерата, за да анализираме съдържанието.")

# Поле за въвеждане на API ключ (за сигурност е скрито)
api_key = st.text_input("Въведете вашия Google Gemini API ключ:", type="password")

if api_key:
    # Конфигуриране на AI модела
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.markdown("---")
    
    # Избор на метод за снимка
    option = st.radio("Изберете как да добавите изображението:", ("Качване на файл", "Снимка с камера"))

    img = None
    if option == "Качване на файл":
        file = st.file_uploader("Качете снимка на етикета", type=["jpg", "jpeg", "png"])
        if file:
            img = Image.open(file)
            st.image(img, caption="Качено изображение", width=400)
    else:
        picture = st.camera_input("Снимайте етикета отблизо")
        if picture:
            img = Image.open(picture)

    # Бутон за стартиране на анализа
    if img and st.button("🔍 Анализирай съставките", type="primary"):
        with st.spinner("Изкуственият интелект чете и анализира етикета... Моля, изчакайте."):
            try:
                # Промпт, който инструктира AI какво точно да направи и какъв формат да върне
                prompt = """
                Разгледай това изображение на етикет на продукт.
                1. Извлечи всички съставки.
                2. Раздели ги на 'Вредна' (потенциално опасни консерванти, изкуствени оцветители, трансмазнини, вредни Е-та, излишна захар и др.) и 'Невредна' (натурални, безопасни, витамини).
                3. За вредните съставки напиши кратко какви са потенциалните отрицателни ефекти за здравето в бъдеще при честа консумация/употреба.
                4. Върни резултата СТРИКТНО във формат JSON със следната структура:
                [
                  {"Съставка": "Име на съставка", "Статус": "Вредна" или "Невредна", "Ефекти": "Описание на ефектите (или 'Няма доказани' за невредните)"}
                ]
                Върни САМО чист JSON код, без никакъв друг текст или форматиране преди и след него.
                """

                # Изпращане на снимката и промпта към модела
                response = model.generate_content([prompt, img])

                # Изчистване на резултата, в случай че AI добави markdown форматиране (```json)
                response_text = response.text.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:-3]
                elif response_text.startswith("```"):
                    response_text = response_text[3:-3]

                # Преобразуване на JSON в Python речник
                data = json.loads(response_text)

                # Създаване на Pandas DataFrame за по-красива таблица
                df = pd.DataFrame(data)

                st.success("Анализът е завършен успешно!")

                # Разделяне на екрана на две колони за визуализация
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🔴 Потенциално вредни")
                    bad_df = df[df["Статус"] == "Вредна"].reset_index(drop=True)
                    if not bad_df.empty:
                        st.dataframe(bad_df[["Съставка", "Ефекти"]], use_container_width=True)
                    else:
                        st.write("Не са открити вредни съставки! 🎉")

                with col2:
                    st.subheader("🟢 Безопасни / Невредни")
                    good_df = df[df["Статус"] == "Невредна"].reset_index(drop=True)
                    if not good_df.empty:
                        st.dataframe(good_df[["Съставка"]], use_container_width=True)
                    else:
                        st.write("Не са открити невредни съставки.")

                st.info("⚠️ **Внимание:** Този анализ е генериран от изкуствен интелект. Класификацията 'вредна' зависи от количеството, индивидуалните алергии и регулациите. Резултатите са само за обща информация и не са медицински съвет.")

            except Exception as e:
                st.error(f"Възникна грешка при анализа. Възможно е снимката да е неясна или AI моделът да се е объркал. Детайли: {e}")
else:
    st.info("👈 Моля, въведете API ключ, за да стартирате приложението. Можете да генерирате безплатен такъв от Google AI Studio (aistudio.google.com).")
